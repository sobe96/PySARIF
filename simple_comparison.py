# simple_comparison.py
import pandas as pd

def compare_simple(df1, df2):
    """Perform a simple comparison between two SARIF DataFrames.

    Args:
        df1 (pd.DataFrame): DataFrame for the first SARIF file.
        df2 (pd.DataFrame): DataFrame for the second SARIF file.

    Returns:
        dict: A dictionary containing the counts and percentages of similarities and differences.
    """
    # Create a unique identifier for each warning/error based on file location and start line
    df1['unique_location'] = df1['File Location'] + ':' + df1['Start Line'].astype(str)
    df2['unique_location'] = df2['File Location'] + ':' + df2['Start Line'].astype(str)

    # Identify common and unique elements
    common = pd.merge(df1, df2, on='unique_location')
    unique_to_df1 = df1[~df1['unique_location'].isin(common['unique_location'])]
    unique_to_df2 = df2[~df2['unique_location'].isin(common['unique_location'])]

    # Calculate counts and percentages
    total_in_df1 = len(df1)
    total_in_df2 = len(df2)
    common_count = len(common)
    unique_to_df1_count = len(unique_to_df1)
    unique_to_df2_count = len(unique_to_df2)

    similarity_percentage = (common_count / (total_in_df1 + total_in_df2)) * 100

    return {
        "total_in_df1": total_in_df1,
        "total_in_df2": total_in_df2,
        "common_count": common_count,
        "unique_to_df1_count": unique_to_df1_count,
        "unique_to_df2_count": unique_to_df2_count,
        "similarity_percentage": similarity_percentage
    }

# You can add more helper functions if needed
