# rule_association.py
import pandas as pd

def associate_rules(df1, df2, output_path):
    """Associate rules between two SARIF DataFrames based on shared exact file locations.

    Args:
        df1 (pd.DataFrame): DataFrame for the first SARIF file.
        df2 (pd.DataFrame): DataFrame for the second SARIF file.
        output_path (str): Path to save the output file.
    """
    # Assuming 'Rule ID' and 'Description' columns exist in the DataFrames
    # Modify as per your DataFrame structure
    df1['unique_location'] = df1['File Location'] + ':' + df1['Start Line'].astype(str)
    df2['unique_location'] = df2['File Location'] + ':' + df2['Start Line'].astype(str)

    # Merge on unique location to find common issues
    common = pd.merge(df1, df2, on='unique_location')

    # Extracting rule association
    rule_association = common[['Rule ID_x', 'Message_x', 'Rule ID_y', 'Message_y']].drop_duplicates(subset=['Rule ID_x', 'Rule ID_y'])
    rule_association.to_csv(f"{output_path}/rule_association.csv", index=False)

    print("Rule association results saved to file.")
