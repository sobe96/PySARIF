import argparse
import json
import requests
import sys
import time


def get_task_status(task_id, token, sonar_url):
    response = requests.get(f"{sonar_url}api/ce/task", params={"id": task_id}, auth=(token, ""))
    response.raise_for_status()
    return response.json()["task"]


def get_analysis_id(task_id, token, sonar_url):
    task_info = get_task_status(task_id, token, sonar_url)
    if task_info["status"] == "SUCCESS":
        return task_info["analysisId"]
    return None


def parse_sonar(project_key, token, sonar_url):
    """Парсинг данных из API SonarQube."""
    auth = (token, '')
    page_size = 500
    params = {
        'components': project_key,
        'p': 1,
        'ps': page_size,
        'impactSoftwareQualities': 'SECURITY, RELIABILITY'
    }

    all_issues = []

    while True:
        response = requests.get(f"{sonar_url}api/issues/search", auth=auth, params=params)
        if response.status_code != 200:
            print(f'Ошибка при запросе: {response.status_code}')
            break
        data = response.json()
        issues = data.get('issues', [])
        all_issues.extend(issues)

        if len(issues) < page_size:
            break

        params['p'] += 1

    return all_issues


def parse_trufflehog(file_path):
    """Парсинг JSON-файла Trufflehog."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Файл {file_path} имеет неверный формат JSON.")
        sys.exit(1)


def convert_to_sarif(issues, mode):
    """Конвертация данных SonarQube в SARIF."""
    name = None
    sem_version = None
    severity_mapping = None
    results = None
    if mode == 'sonar':
        severity_mapping = {
            'BLOCKER': 'Critical',
            'CRITICAL': 'Critical',
            'MAJOR': 'Major',
            'MINOR': 'Medium',
            'INFO': 'Minor'
        }
        name = "SonarQube"
        sem_version = "10.7"
    elif mode == 'trufflehog':
        severity_mapping = {
            # сделать маппинг статусов
        }
        name = "Trufflehog"
        sem_version = "3.86.0"
    sarif_template = {
        "$schema": "http://json.schemastore.org/sarif-2.1.0",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": name,
                    "semanticVersion": sem_version
                }
            },
            "results": []
        }]
    }
    if mode == 'sonar':
        results = sonar_data_add_to_sarif(issues, severity_mapping)
    if mode == 'trufflehog':
        results = trufflehog_data_add_to_sarif(issues)

    if results:
        sarif_template['runs'][0]['results'] = results
    return sarif_template, len(results)


def sonar_data_add_to_sarif(issues, severity_mapping):
    results = []
    print(len(issues['issues']))
    for issue in issues['issues']:
        print(issue)
        result = {
            "ruleId": issue['rule'],
            "level": severity_mapping.get(issue['severity'], 'Undecided'),
            "message": {
                "text": issue['message']
            },
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": issue['component']
                    },
                    "region": {
                        "startLine": issue.get('line', 1)
                    }
                }
            }]
        }
        results.append(result)

    return results


def trufflehog_data_add_to_sarif(issues):
    """Конвертация данных Trufflehog в SARIF."""
    results = []
    for issue in issues:
        result = {
            "ruleId": issue["DetectorName"],
            "message": {"text": issue["DetectorDescription"]},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": issue["SourceMetadata"]["Data"]["Git"][
                                "file"
                            ]
                        },
                        "region": {
                            "startLine": issue["SourceMetadata"]["Data"][
                                "Git"
                            ]["line"],
                        },
                    }
                }
            ]
        }
        results.append(result)

    return results


def save_sarif(sarif, project_key, runner='unspecified'):
    """Сохранение SARIF в файл."""
    output_file = f'{project_key}-{runner}.sarif'
    with open(output_file, 'w') as f:
        json.dump(sarif, f, indent=4)
    print(f"SARIF успешно сохранен: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Парсер для SonarQube и Trufflehog")
    parser.add_argument("mode", choices=["sonar", "trufflehog"], help="Режим работы")
    parser.add_argument(
        "--taskid",
        help="ID задачи SonarQube (только для режима 'sonar')",
    )
    parser.add_argument(
        "--data",
        help="Путь к JSON-файлу с результатами Trufflehog (только для режима 'trufflehog')",
    )
    parser.add_argument(
        "--sonartoken", help="Токен доступа к SonarQube (только для режима 'sonar')"
    )
    parser.add_argument(
        "--sonarhost", help="Адрес API Endpoint для SonarQube (только для режима 'sonar')"
    )
    parser.add_argument(
        '--project', type=str, help="Название проекта в GitLab для корректного создания имени SARIF"
    )
    parser.add_argument(
        '--runner', type=str, help='Runner, используемый в GitLab для корректного создания имени SARIF'
    )
    args = parser.parse_args()

    if args.runner:
        runner = args.runner
        print(f"Имя runner'а: {runner}")
    else:
        runner = "unknown_runner"
        print(f"Runner не определен. Используется имя runner'а: {runner}")
    if args.project:
        project_key = args.project
        print(f"Имя проекта: {project_key}")
    else:
        project_key = "unknown_project"
        print(f"Имя проекта не определено. Используется имя проекта: {project_key}")

    if args.mode == "sonar":
        sonar_token = args.sonartoken
        sonar_host = args.sonarhost
        if not sonar_token:
            print("Для режима 'sonar' необходимо указать --sonartoken.")
            sys.exit(1)
        if not sonar_host:
            print("Для режима 'sonar' необходимо указать --sonarhost.")
            sys.exit(1)
        if args.taskid:
            task_id = args.taskid
            print(f"SonarQube TaskID: {task_id}")
            analysis_id = None
            while not analysis_id:
                task_info = get_task_status(task_id, sonar_token, sonar_host)
                if task_info["status"] == "SUCCESS":
                    analysis_id = get_analysis_id(task_id, sonar_token, sonar_host)
                if not analysis_id:
                    print("Анализ еще не завершен. Ожидание...")
                    time.sleep(10)
                if task_info["status"] == "FAILED":
                    print("Анализ завершился неудачей. Завершение...")
                    sys.exit(1)

            all_issues = parse_sonar(project_key, sonar_token, sonar_host)
            sarif, num_results = convert_to_sarif({'issues': all_issues}, args.mode)

            print(f'Количество результатов: {num_results}')
        else:
            print("Для режима 'sonar' необходимо указать --taskid.")
            return

    elif args.mode == "trufflehog":
        if not args.data:
            print("Для режима 'trufflehog' необходимо указать --data.")
            sys.exit(1)
        data = parse_trufflehog(args.data)
        sarif, num_results = convert_to_sarif(data, args.mode)

        print(f'Количество результатов: {num_results}')
    else:
        print("Необходимо указать sonar или trufflehog в вызове скрипта")
        return
    if sarif:
        save_sarif(sarif, project_key, runner)


if __name__ == "__main__":
    main()
