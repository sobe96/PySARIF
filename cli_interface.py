# cli_interface.py
import file_reader
import dataframe_manager
import data_analysis
import utils
import os

def main_menu():
    while True:
        print("\nPySarif Engineer")
        print("1. Load SARIF File as Pandas DataFrame")
        print("2. Analyze Data")
        print("3. Save DataFrame as .csv")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            load_sarif_file()
        elif choice == '2':
            analyze_data()
        elif choice == '3':
            save_data()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def load_sarif_file():
    global file_path
    file_path = input("Enter the path to the SARIF file: ")
    sarif_data = file_reader.read_sarif_file(file_path)
    global parsed_issues
    parsed_issues = dataframe_manager.create_issues_dataframe(sarif_data)
    print("File loaded successfully:")


def analyze_data():
    if parsed_issues.empty:
        print("No data to analyze. Please load a SARIF file first.")
        return
    analysis_results = data_analysis.summarize_issues(parsed_issues)
    print(analysis_results)


def save_data():
    if parsed_issues.empty:
        print("No data to save. Please load a SARIF file first.")
        return

    file_name = utils.get_file_name_without_extension(file_path)
    utils.save_csv(parsed_issues, file_name)
    print(f"Saved successfully as {file_name}.csv")


if __name__ == '__main__':
    main_menu()
