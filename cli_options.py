import file_hierarchy
import file_reader
import dataframe_manager
import data_analysis
import utils
import simple_comparison
import advanced_comparison
import rule_association
import manual_trim
import tkinter as tk
from tkinter import filedialog
import os


def load_sarif_file(file_path, need_print):
    sarif_data = file_reader.read_sarif_file(file_path)
    dataframe = dataframe_manager.create_sarif_dataframe(sarif_data)
    if need_print:
        dataframe = file_hierarchy.build_and_print_hierarchy(dataframe)
        print("File loaded successfully:")
    return dataframe


def load_csv_file(file_path, need_print):
    csv_data = file_reader.read_csv_file(file_path)
    dataframe = dataframe_manager.create_csv_dataframe(csv_data)
    if need_print:
        dataframe = file_hierarchy.build_and_print_hierarchy(dataframe)
        print("File loaded successfully:")
    return dataframe


def gui_select(dataframes, extension):
    root = tk.Tk()
    root.withdraw()
    need_print = True
    file_path = filedialog.askopenfilename(filetypes=[("DATA files", f"*.{extension}")])
    if file_path:
        print(f'Loading {file_path}...')
        file_name = utils.get_file_name_without_extension(file_path)
        if extension == 'sarif':
            dataframes[file_name] = load_sarif_file(file_path, need_print)
        elif extension == 'csv':
            dataframes[file_name] = load_csv_file(file_path, need_print)

    return dataframes


def analyze_data(dataframes):
    for file_name, df in dataframes.items():
        if df.empty:
            print(f"No data to analyze for {file_name}.")
            return
        analysis_results = data_analysis.summarize_issues(df)
        print(f"Analysis Results for {file_name}:")
        print(analysis_results)


def trim_dataframes(dataframes):
    if len(dataframes) < 2:
        print("At least two SARIF files are required for comparison.")
        return

    print("Select two SARIF files for comparison.")
    print("Available files:", list(dataframes.keys()))
    file1 = input("Enter the name of the first SARIF file: ")
    file2 = input("Enter the name of the second SARIF file: ")

    if file1 not in dataframes or file2 not in dataframes:
        print("One or both SARIF files not found.")
        return

    dataframes[file1] = file_hierarchy.build_and_print_hierarchy(dataframes[file1])
    dataframes[file2] = file_hierarchy.build_and_print_hierarchy(dataframes[file2])
    print(f'Trimming {file1}')
    dataframes[file1] = manual_trim.manual_trim_paths(dataframes[file1], file1)
    print(f'Trimming {file2}')
    dataframes[file2] = manual_trim.manual_trim_paths(dataframes[file2], file2)

    return dataframes


def save_data(dataframes):
    dir = 'data/processed_csv'
    for file_name, df in dataframes.items():
        if df.empty:
            print(f"No data to save for {file_name}. Please load a SARIF file first.")
            return

        utils.save_csv(df, file_name, dir)
        print(f"Saved successfully as {file_name}.csv at {dir}")


def compare_sarif_files(dataframes):
    if len(dataframes) < 2:
        print("At least two SARIF files are required for comparison.")
        return

    print("Select two SARIF files for comparison.")
    print("Available files:", list(dataframes.keys()))
    file1 = input("Enter the name of the first SARIF file: ")
    file2 = input("Enter the name of the second SARIF file: ")

    if file1 not in dataframes or file2 not in dataframes:
        print("One or both SARIF files not found.")
        return

    print("1. Simple Comparison\n2. Advanced Comparison")
    choice = input("Choose comparison mode: ")
    # Call to simple comparison function
    if choice == '1':
        result = simple_comparison.compare_simple(dataframes[file1], dataframes[file2])
        print("Simple Comparison Result:")
        print(result)

    # Call to advanced comparison function
    elif choice == '2':
        output_path = "outputs"  # Set your output directory
        advanced_comparison.compare_advanced(dataframes[file1], dataframes[file2], output_path, file1,
                                             file2)
        rule_association.associate_rules(dataframes[file1], dataframes[file2], output_path, file1, file2)


def find_substring_in_list(array_of_strings, checked_string):
    found_string = None
    for string in array_of_strings:
        if string in checked_string:
            found_string = string
            break
    return found_string


def auto_trim():
    filename = 'projects.txt'
    base_dir = 'data/trim'
    save_dir = 'data/processed'
    projects = []
    need_print = False
    with open(filename) as file:
        while line := file.readline():
            projects.append(line.rstrip())
    if len(projects) < 1:
        print(f"{filename} is empty")
        return
    print(projects)
    for item in os.listdir(base_dir):
        if item.endswith('.sarif'):
            file_name = utils.get_file_name_without_extension(item)
            item_path = os.path.join(base_dir, item)
            dataframe = load_sarif_file(item_path, need_print)
            dataframe = file_hierarchy.check_path(dataframe)
            prefix = find_substring_in_list(projects, file_name)
            dataframe = manual_trim.remove_prefix_and_parents(dataframe, prefix)
            utils.save_csv(dataframe, file_name, save_dir)
            print(f'{prefix} done!')
