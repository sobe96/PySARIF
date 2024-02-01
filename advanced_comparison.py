# advanced_comparison.py
import pandas as pd

def compare_advanced(df1, df2, output_path):
    """Perform an advanced comparison between two SARIF DataFrames and output results to files.

    Args:
        df1 (pd.DataFrame): DataFrame for the first SARIF file.
        df2 (pd.DataFrame): DataFrame for the second SARIF file.
        output_path (str): Path to save the output files.
    """
    df1['unique_location'] = df1['File Location'] + ':' + df1['Start Line'].astype(str)
    df2['unique_location'] = df2['File Location'] + ':' + df2['Start Line'].astype(str)

    # Identify common and unique elements
    common = pd.merge(df1, df2, on='unique_location')
    unique_to_df1 = df1[~df1['unique_location'].isin(common['unique_location'])].drop_duplicates(subset=["Rule ID"])
    unique_to_df2 = df2[~df2['unique_location'].isin(common['unique_location'])].drop_duplicates(subset=["Rule ID"])

    # Output to files
    common.to_csv(f"{output_path}/common_issues.csv", index=False)
    unique_to_df1.to_csv(f"{output_path}/unique_to_df1_issues.csv", index=False)
    unique_to_df2.to_csv(f"{output_path}/unique_to_df2_issues.csv", index=False)

    print("Advanced comparison results saved to files.")
