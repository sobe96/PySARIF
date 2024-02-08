# file_reader.py
import json


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
