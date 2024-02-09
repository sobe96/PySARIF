# cli_interface.py
import cli_options

dataframes = {}


def main_menu():
    while True:
        print("\nPySarif Engineer")
        print("1. Load SARIF File as Pandas DataFrame")
        print("2. Load Svace CSV File as Pandas DataFrame")
        print("3. Trim data")
        print("4. Analyze Data")
        print("5. Save DataFrame as .csv")
        print("6. Compare SARIF Files")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            cli_options.gui_select(dataframes, 'sarif')
        elif choice == '2':
            cli_options.gui_select(dataframes, 'csv')
        elif choice == '3':
            cli_options.trim_dataframes(dataframes)
        elif choice == '4':
            cli_options.analyze_data(dataframes)
        elif choice == '5':
            cli_options.save_data(dataframes)
        elif choice == '6':
            cli_options.compare_sarif_files(dataframes)
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main_menu()
