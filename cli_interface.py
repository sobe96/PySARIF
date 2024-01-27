# cli_interface.py
import file_reader
import dataframe_manager
import data_analysis
import utils
import simple_comparison
import advanced_comparison
import rule_association

sarif_dataframes = {}
def main_menu():
    while True:
        print("\nPySarif Engineer")
        print("1. Load SARIF File as Pandas DataFrame")
        print("2. Analyze Data")
        print("3. Save DataFrame as .csv")
        print("4. Compare SARIF Files")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            load_sarif_file()
        elif choice == '2':
            analyze_data()
        elif choice == '3':
            save_data()
        elif choice == '4':
            compare_sarif_files()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def load_sarif_file():
    global file_path
    file_path = input("Enter the path to the SARIF file: ")
    file_name = utils.get_file_name_without_extension(file_path)
    sarif_data = file_reader.read_sarif_file(file_path)
    global parsed_issues
    sarif_dataframes[file_name] = dataframe_manager.create_issues_dataframe(sarif_data)
    prefixes = [
        "file:///sast/packages-to-analyze/linux-astra-modules-5.10/linux-astra-modules-5.10-5.10.190",
        "file:///"
    ]
    for prefix in prefixes:
        sarif_dataframes[file_name] = utils.remove_specific_prefix(sarif_dataframes[file_name], 'File Location', prefix)
    print("File loaded successfully:")


def analyze_data():
    for file_name, df in sarif_dataframes.items():
        if df.empty:
            print(f"No data to analyze for {file_name}.")
            return
        analysis_results = data_analysis.summarize_issues(df)
        print(f"Analysis Results for {file_name}:")
        print(analysis_results)


def save_data():
    for file_name, df in sarif_dataframes.items():
        if df.empty:
            print(f"No data to save for {file_name}. Please load a SARIF file first.")
            return

        utils.save_csv(df, file_name)
        print(f"Saved successfully as {file_name}.csv")

def compare_sarif_files():
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
        advanced_comparison.compare_advanced(sarif_dataframes[file1], sarif_dataframes[file2], output_path)
        rule_association.associate_rules(sarif_dataframes[file1], sarif_dataframes[file2], output_path)
    # Call to advanced comparison function


if __name__ == '__main__':
    main_menu()
