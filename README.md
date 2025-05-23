# PySarifTool
## Описание
PySarifTool — это инструмент на Python для анализа файлов SARIF (формат обмена результатами статического анализа). Он предоставляет функции для чтения, парсинга и манипуляции данными SARIF, что облегчает интерпретацию и сравнение результатов статического анализа.
## Возможности
- Проверка путей: Валидация и изменение путей файлов в журналах SARIF.
- Анализ данных: Проведение простых и сложных сравнений данных SARIF.
- Интерфейс CLI: Командный интерфейс для удобного взаимодействия с инструментом.
- Управление данными: Инструменты для управления данными и анализа иерархических файловых структур.
## Установка
Для установки PySarifTool клонируйте репозиторий и используйте pip:
```
git clone <link to repo>
cd PySARIF
# Создайте venv, если требуется
pip3 install -r requirements.txt
```
## Использование
Запустите основной скрипт для начала использования инструмента:
```
python main.py
```
Станут доступны опции для работы с инструментом:
- Load SARIF File as Pandas DataFrame
  - В контекстном окне выбрать .sarif файл, чтобы загрузить его для дальнейших действий
- Load Svace CSV File as Pandas DataFrame 
  - В контекстном окне выбрать .csv файл от Svace, чтобы загрузить его для дальнейших действий
- Trim data
  - Выбрать 2 загруженных ранее файла для усечения путей, если есть такая необходимость (полезно для более эффективного 
  и точного анализа)
- Analyze Data
  - Выводит в командную строку простую сводку по каждому загруженному файлу с описанием количества срабатываний и 
  наиболее частых чекеров
- Save DataFrame as .csv
  - Сохранить в .csv формате со всеми изменениями
- Compare SARIF Files
  - Выбрать 2 загруженных ранее файла для проведения анализа. Доступны Простой анализ и Продвинутый анализ.
    - Простой анализ предоставляет вывод в командную строку статистических данных, касающихся сравнения двух выбранных 
    файлов. 
    - Продвинутый анализ выводит в директорию outputs несколько таблиц
      - common_issues - срабатывания двух разных анализаторов, которые были найдены в одном месте.
      - detailed_summary - показывает, какие срабатывания разных анализаторов совпали, какое количество таких типов 
      срабатываний было в каждом файле, и какое количество срабатываний такого типа оба файла совпадают.
      - rule_association - приводит названия срабатываний, которые скрипт считает одинаковыми чекерами от разных 
      анализаторов
      - unique - создается для каждого файла и, наоборот, показывает срабатывания для каждого анализатора, которые не 
      совпали ни в одном случае при сравнении файлов анализа
    - Сравнивать таким образом можно .csv и .sarif одновременно. 
- Trim every .sarif in data/trim
  - Автоматический режим усечения путей, в котором сперва нужно положить .sarif файлы в data/trim и прописать названия 
  пакетов в projects.txt ровно так, как они назывались при анализе. Данный способ обрезки путей автоматический, но 
  предоставляет только возможность сохранения итоговых данных в формате csv.
- Exit
  - Завершение работы инструмента
# PySarifPathChecker
## Важно!
Для корректной работы скрипта названия SARIF-файлов должны соответствовать маске {project}-{sastTool}.sarif
Например, libvirt-svace.sarif. В 'project' должно входить полное название, например: parsec-3.4+ci38 (точно так же, 
арумент --project или строка в --projects_file тоже должны быть parsec-3.4+ci38, соответственно). Иначе есть 
вероятность, что пути не будут полностью обработаны.
## Описание
Скрипт, который автоматически исправляет пути в sarif файлах, основываясь либо на файле ../projects.txt, либо на 
передаваемом при вызове команды аргументе. На выходе получаем .sarif с исправленными путями.
## Использование
### Запускаем скрипт с аргументами:
- --folder: Путь к папке, содержащей .sarif файлы (по умолчанию ../data/backup).
- --file: Путь к одному .sarif файлу.
- --project: Имя проекта для использования напрямую.
- --projects_file: Путь к файлу с названиями проектов (по умолчанию ../projects.txt, который необходимо заранее создать и заполнить).
### Обработка в зависимости от аргументов:
- Если указан --project, используется это имя проекта.
- Если указан --projects_file, используются названия проектов внутри текстового файла с названиями проектов.
- Если указан --folder, обрабатываются все файлы в папке.
- Если указан --file, обрабатывается только этот файл.
```
python3 SarifReader.py --project project_name --file project_name-runner_name.sarif
```
# GetSarif
## Описание
Данный скрипт разработан для создания SARIF-файлов срабатываний Trufflehog или SonarQube.
Для Trufflehog на вход подается JSON-отчет. Для SonarQube используется API SonarQube.
## Использование
### Запускаем скрипт с аргументами:
- на данный момент mode может быть только sonar или trufflehog.
- При создании SARIF из срабатываний SonarQube необходимо указать:
  * --sonartoken: API-access токен для SonarQube (вида sqa_...).
  * --sonarhost: URL SonarQube (http://sonarhost:port/)
  * --taskid: TaskID из лога SonarQube (можно получить, например, вот так: TASK_ID=$(grep "ce/task?id" your_SonarQube_log.txt | cut -d "=" -f 2))
- При создании SARIF из отчета Trufflehog необходимо указать:
  * --data: Путь к JSON-отчету с результатами Trufflehog
- --project: Название проекта для корректного создания имени SARIF (по умолчанию: unknown_project)
- --runner: Название Gitlab runner'а для корректного создания имени SARIF (по умолчанию: unknown_runner)
### Пример
Для SonarQube
```
python3 get_sarif.py sonar --sonartoken sqa_token --sonarhost http://sonarhost:port/ --project project_name --taskid task_id-sonarqube --runner runner_name
```
Для Trufflehog
```
python3 get_sarif.py trufflehog --data path/to/trufflehog/report.json --project project_name --runner runner_name
```