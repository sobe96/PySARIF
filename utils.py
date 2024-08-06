import pandas as pd
from collections import Counter
import os


def get_common_prefixes(df, file_path_column, depth):
    """Find the most common prefixes in file paths up to a specified depth."""
    # Split each path and take the first 'depth' parts
    prefixes = ['/'.join(path.split('/')[:depth]) for path in df[file_path_column]]

    # Count the occurrences of each prefix
    prefix_counts = Counter(prefixes)

    # Get the most common prefixes
    most_common = prefix_counts.most_common()

    return most_common


def remove_specific_prefix(df, file_path_column, prefix):
    """Remove a specific prefix from file paths in the DataFrame."""
    if not prefix.endswith('/'):
        prefix += '/'

    def trim_prefix(path):
        # Check if the path starts with the prefix and remove it
        if path.startswith(prefix):
            return path.replace(prefix, '/', 1)  # Replace the first occurrence only
        return path
    df[file_path_column] = df[file_path_column].apply(trim_prefix)
    return df


def check_duplicates(df):
    duplicate_rows = df.duplicated()

    # Count the number of duplicate rows
    num_duplicates = duplicate_rows.sum()
    print(f"Number of duplicate rows: {num_duplicates}")

    # Optional: Display the duplicate rows
    if num_duplicates > 0:
        print("Duplicate Rows:")
        print(df[duplicate_rows])


def get_file_name_without_extension(file_path):
    """Get the file name without extension from a file path.

    Args:
        file_path (str): The full path of the file.

    Returns:
        str: The file name without the extension.
    """
    base_name = os.path.basename(file_path)  # Extracts the file name with extension
    file_name_without_extension = os.path.splitext(base_name)[0]  # Splits the extension and takes the name part
    return file_name_without_extension


def save_csv(df, file_name, path):
    df.to_csv(f"{path}/{file_name}.csv", index=False)
