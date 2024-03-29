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




def load_sarif_file(sarif_dataframes):
    # global file_path
    # file_path = input("Enter the path to the SARIF file: ")
    file_name = utils.get_file_name_without_extension(file_path)
    sarif_data = file_reader.read_sarif_file(file_path)
    sarif_dataframes[file_name] = dataframe_manager.create_sarif_dataframe(sarif_data)
    #prefixes = [
    #    "file:///sast/packages-to-analyze/linux-astra-modules-5.10/linux-astra-modules-5.10-5.10.190",
    #    "file:///"
    #]
    #for prefix in prefixes:
    #    sarif_dataframes[file_name] = utils.remove_specific_prefix(sarif_dataframes[file_name], 'File Location', prefix)

    file_hierarchy.build_and_print_hierarchy(sarif_dataframes[file_name])
    #manual_trim.manual_trim_paths(sarif_dataframes[file_name])
    print("File loaded successfully:")


def load_csv_file(dataframes):
    file_name = utils.get_file_name_without_extension(file_path)
    csv_data = file_reader.read_csv_file(file_path)
    dataframes[file_name] = dataframe_manager.create_csv_dataframe(csv_data)
    file_hierarchy.build_and_print_hierarchy(dataframes[file_name])
    #manual_trim.manual_trim_paths((dataframes[file_name]))
    print("File loaded successfully:")


def gui_select(dataframes, extension):
    global file_path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("DATA files", f"*.{extension}")])
    if file_path:
        print(f'Loading {file_path}...')
        if extension == 'sarif':
            load_sarif_file(dataframes)
        elif extension == 'csv':
            load_csv_file(dataframes)

def analyze_data(sarif_dataframes):
    for file_name, df in sarif_dataframes.items():
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

    file_hierarchy.build_and_print_hierarchy(dataframes[file1])
    file_hierarchy.build_and_print_hierarchy(dataframes[file2])
    print(f'Trimming {file1}')
    dataframes[file1] = manual_trim.manual_trim_paths(dataframes[file1], file1)
    print(f'Trimming {file2}')
    dataframes[file2] = manual_trim.manual_trim_paths(dataframes[file2], file2)


def save_data(sarif_dataframes):
    for file_name, df in sarif_dataframes.items():
        if df.empty:
            print(f"No data to save for {file_name}. Please load a SARIF file first.")
            return

        utils.save_csv(df, file_name)
        print(f"Saved successfully as {file_name}.csv")


def compare_sarif_files(sarif_dataframes):
    if len(sarif_dataframes) < 2:
        print("At least two SARIF files are required for comparison.")
        return

    print("Select two SARIF files for comparison.")
    print("Available files:", list(sarif_dataframes.keys()))
    file1 = input("Enter the name of the first SARIF file: ")
    file2 = input("Enter the name of the second SARIF file: ")

    if file1 not in sarif_dataframes or file2 not in sarif_dataframes:
        print("One or both SARIF files not found.")
        return

    print("1. Simple Comparison\n2. Advanced Comparison")
    choice = input("Choose comparison mode: ")

    if choice == '1':
        result = simple_comparison.compare_simple(sarif_dataframes[file1], sarif_dataframes[file2])
        print("Simple Comparison Result:")
        print(result)
    # Call to simple comparison function
    elif choice == '2':
        output_path = "outputs"  # Set your output directory
        advanced_comparison.compare_advanced(sarif_dataframes[file1], sarif_dataframes[file2], output_path, file1,
                                             file2)
        rule_association.associate_rules(sarif_dataframes[file1], sarif_dataframes[file2], output_path, file1, file2)

    # Call to advanced comparison function
