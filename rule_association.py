# rule_association.py
import pandas as pd


def associate_rules(df1, df2, output_path, filename1, filename2):
    """Associate rules between two SARIF DataFrames based on shared exact file locations.

    Args:
        df1 (pd.DataFrame): DataFrame for the first SARIF file.
        df2 (pd.DataFrame): DataFrame for the second SARIF file.
        output_path (str): Path to save the output file.
    """
    # Count rule occurrences in each DataFrame before merge
    rule_counts_df1 = df1['Rule ID'].value_counts().reset_index().rename(
        columns={'index': f'Rule ID_{filename1}', 'Rule ID': f'Initial_count_{filename1}'})
    rule_counts_df2 = df2['Rule ID'].value_counts().reset_index().rename(
        columns={'index': f'Rule ID_{filename2}', 'Rule ID': f'Initial_count_{filename2}'})

    # Assuming 'Rule ID' and 'Description' columns exist in the DataFrames
    # Modify as per your DataFrame structure
    df1['unique_location'] = df1['File Location'] + ':' + df1['Start Line'].astype(str)
    df2['unique_location'] = df2['File Location'] + ':' + df2['Start Line'].astype(str)

    # Merge on unique location to find common issues
    common = pd.merge(df1, df2, on='unique_location', suffixes=(f'_{filename1}',f'_{filename2}'))

    # Extracting rule association
    duplicates_count = common.groupby([f'Rule ID_{filename1}', f'Rule ID_{filename2}']).size().reset_index(
        name=f'Mutual_count_{filename1}_and_{filename2}')

    detailed_summary = pd.merge(duplicates_count, rule_counts_df1, on=f'Rule ID_{filename1}', how='left')
    detailed_summary = pd.merge(detailed_summary, rule_counts_df2, on=f'Rule ID_{filename2}', how='left')

    rule_association = common[[f'Rule ID_{filename1}', f'Rule ID_{filename2}']].drop_duplicates(
        subset=[f'Rule ID_{filename1}', f'Rule ID_{filename2}'])

    # Save rule association
    rule_association.to_csv(f"{output_path}/rule_association_{filename1}_{filename2}.csv",
                            mode="a", index=False)
    df = pd.read_csv(f"{output_path}/rule_association_{filename1}_{filename2}.csv")
    df = df.drop_duplicates()
    df.to_csv(f"{output_path}/rule_association_{filename1}_{filename2}.csv", index=False)

    detailed_summary.to_csv(f"{output_path}/detailed_summary_{filename1}_{filename2}.csv", index=False)

    print("Rule association results saved to file.")
