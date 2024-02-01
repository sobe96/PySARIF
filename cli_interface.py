# cli_interface.py
import cli_options

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
            cli_options.load_sarif_file(sarif_dataframes)
        elif choice == '2':
            cli_options.analyze_data(sarif_dataframes)
        elif choice == '3':
            cli_options.save_data(sarif_dataframes)
        elif choice == '4':
            cli_options.compare_sarif_files(sarif_dataframes)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
