# file_reader.py
import json
import pandas as pd


def read_sarif_file(file_path):
    """Read and parse a SARIF file.

    Args:
        file_path (str): Path to the SARIF file.

    Returns:
        dict: Parsed JSON data from the SARIF file or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as file:
            sarif_data = json.load(file)
            return sarif_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading SARIF file: {e}")
        return None


def read_csv_file(csv_file_path):
    """Read a CSV file and load its data into a pandas DataFrame.

    Args:
        csv_file_path (str): The file path of the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the CSV file, or None if an error occurs.
    """
    try:
        df = pd.read_csv(csv_file_path)
        # Perform any initial preprocessing required:
        # For example, renaming columns to match the structure expected by comparison functions.
        # df.rename(columns={'original_column_name': 'new_column_name'}, inplace=True)

        return df
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"No data: The file is empty - {csv_file_path}")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
