import os
import json
import glob
import argparse


def process_sarif_file(filepath, project_name):
    print(filepath)

    def clean_uri(uri, project_name, project_index):
        if project_index != -1:
            uri = uri[project_index + len(project_name):]
        # Убираем 'file://' в начале
        if uri.startswith('file://'):
            uri = uri[7:]
        # Добавляем '/' в начале, если нет
        if not uri.startswith('/'):
            uri = '/' + uri
        #if not uri.startswith(f'/{project_name}'):
        #    uri = f'/{project_name}' + uri
        return uri

    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Проходим по всем результатам анализа и обрезаем пути
    if 'runs' in data:
        for run in data['runs']:
            if 'results' in run:
                for result in run['results']:
                    if 'locations' in result:
                        for location in result['locations']:
                            if 'physicalLocation' in location and 'artifactLocation' in location['physicalLocation']:
                                uri = location['physicalLocation']['artifactLocation'].get('uri', '')
                                project_index = uri.find(project_name)
                                uri = clean_uri(uri, project_name, project_index)
                                location['physicalLocation']['artifactLocation']['uri'] = uri

                    if 'codeFlows' in result:
                        for code_flow in result['codeFlows']:
                            if 'threadFlows' in code_flow:
                                for thread_flow in code_flow['threadFlows']:
                                    if 'locations' in thread_flow:
                                        for location in thread_flow['locations']:
                                            if 'location' in location:
                                                if isinstance(location['location'], list):
                                                    for loc in location['location']:
                                                        if 'physicalLocation' in loc and 'artifactLocation' in loc['physicalLocation']:
                                                            uri = loc['physicalLocation']['artifactLocation'].get('uri', '')
                                                            project_index = uri.find(project_name)
                                                            uri = clean_uri(uri, project_name, project_index)
                                                            loc['physicalLocation']['artifactLocation']['uri'] = uri

                                                else:
                                                    loc = location['location']
                                                    if 'physicalLocation' in loc and 'artifactLocation' in loc['physicalLocation']:
                                                        uri = loc['physicalLocation']['artifactLocation'].get('uri', '')
                                                        project_index = uri.find(project_name)
                                                        uri = clean_uri(uri, project_name, project_index)
                                                        loc['physicalLocation']['artifactLocation']['uri'] = uri

    # Сохраняем изменения обратно в файл
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def process_folder(folder_path, project_names):
    # Ищем все .sarif файлы в указанной папке
    sarif_files = glob.glob(os.path.join(folder_path, '*.sarif'))

    for sarif_file in sarif_files:
        # Определяем название проекта по имени файла
        basename = os.path.basename(sarif_file)
        for project_name in project_names:
            if project_name in basename:
                process_sarif_file(sarif_file, project_name)
                break


def load_project_names(projects_file):
    with open(projects_file, 'r', encoding='utf-8') as file:
        return sorted([line.strip() for line in file.readlines()], key=len, reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Process SARIF files to adjust URIs.")
    parser.add_argument('--folder', type=str, default='../data/backup/',
                        help="Path to the folder containing SARIF files.")
    parser.add_argument('--file', type=str, help="Path to a single SARIF file.")
    parser.add_argument('--project', type=str, help="Project name to be used directly.")
    parser.add_argument('--projects_file', type=str, default='../projects.txt',
                        help="Path to the file containing project names.")

    args = parser.parse_args()

    if args.project:
        project_names = [args.project]
    else:
        project_names = load_project_names(args.projects_file)

    if args.file:
        basename = os.path.basename(args.file)
        for project_name in project_names:
            if project_name in basename:
                process_sarif_file(args.file, project_name)
                break
    else:
        process_folder(args.folder, project_names)


if __name__ == "__main__":
    main()