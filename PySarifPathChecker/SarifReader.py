import os
import json
import glob

def process_sarif_file(filepath, project_name):
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
                                if project_index != -1:
                                    location['physicalLocation']['artifactLocation']['uri'] = '/' + uri[project_index:]
                                if location['physicalLocation']['artifactLocation']['uri'].startswith('file://'):
                                    location['physicalLocation']['artifactLocation']['uri'] = location['physicalLocation']['artifactLocation']['uri'][7:]
                                if not (location['physicalLocation']['artifactLocation']['uri'].startswith('/')):
                                    location['physicalLocation']['artifactLocation']['uri'] = '/' + location['physicalLocation']['artifactLocation']['uri']
                                if not location['physicalLocation']['artifactLocation'][
                                    'uri'].startswith(f'/{project_name}'):
                                    location['physicalLocation']['artifactLocation'][
                                        'uri'] = f'/{project_name}' + location['physicalLocation']['artifactLocation'][
                                        'uri']

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
                                                            if project_index != -1:
                                                                loc['physicalLocation']['artifactLocation']['uri'] = '/' + uri[project_index:]
                                                            if loc['physicalLocation']['artifactLocation'][
                                                                'uri'].startswith('file://'):
                                                                loc['physicalLocation']['artifactLocation'][
                                                                    'uri'] = \
                                                                loc['physicalLocation']['artifactLocation']['uri'][
                                                                7:]
                                                            if not (loc['physicalLocation']['artifactLocation'][
                                                                'uri'].startswith('/')):
                                                                loc['physicalLocation']['artifactLocation'][
                                                                    'uri'] = '/' + loc['physicalLocation'][
                                                                    'artifactLocation']['uri']
                                                            if not loc['physicalLocation']['artifactLocation'][
                                                                'uri'].startswith(f'/{project_name}'):
                                                                loc['physicalLocation']['artifactLocation'][
                                                                    'uri'] = f'/{project_name}' + loc['physicalLocation']['artifactLocation'][
                                                                'uri']
                                                else:
                                                    loc = location['location']
                                                    if 'physicalLocation' in loc and 'artifactLocation' in loc['physicalLocation']:
                                                        uri = loc['physicalLocation']['artifactLocation'].get('uri', '')
                                                        project_index = uri.find(project_name)
                                                        if project_index != -1:
                                                            loc['physicalLocation']['artifactLocation']['uri'] = '/' + uri[project_index:]
                                                        if loc['physicalLocation']['artifactLocation'][
                                                            'uri'].startswith('file://'):
                                                            loc['physicalLocation']['artifactLocation']['uri'] = \
                                                            loc['physicalLocation']['artifactLocation']['uri'][7:]
                                                        if not (loc['physicalLocation']['artifactLocation'][
                                                            'uri'].startswith('/')):
                                                            loc['physicalLocation']['artifactLocation'][
                                                                'uri'] = '/' + loc['physicalLocation'][
                                                                'artifactLocation']['uri']
                                                        if not loc['physicalLocation']['artifactLocation'][
                                                            'uri'].startswith(f'/{project_name}'):
                                                            loc['physicalLocation']['artifactLocation'][
                                                                'uri'] = f'/{project_name}' + \
                                                                         loc['physicalLocation']['artifactLocation'][
                                                                             'uri']

    # Сохраняем изменения обратно в файл
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def main(folder_path, projects_file):
    # Считываем названия проектов из файла и сортируем по убыванию длины
    with open(projects_file, 'r', encoding='utf-8') as file:
        project_names = sorted([line.strip() for line in file.readlines()], key=len, reverse=True)

    # Ищем все .sarif файлы в указанной папке
    sarif_files = glob.glob(os.path.join(folder_path, '*.sarif'))

    for sarif_file in sarif_files:
        # Определяем название проекта по имени файла
        basename = os.path.basename(sarif_file)
        for project_name in project_names:
            if project_name in basename:
                process_sarif_file(sarif_file, project_name)
                break

if __name__ == "__main__":
    folder_path = '../data/backup'  # Укажите путь к папке с .sarif файлами
    projects_file = '../projects.txt'  # Укажите путь к файлу с названиями проектов
    main(folder_path, projects_file)