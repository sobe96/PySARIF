# data_analysis.py
from collections import Counter
import json
import pandas as pd
# data_analysis.py
import pandas as pd

def summarize_issues(issues_df):
    """Summarize issues from a Pandas DataFrame.

    Args:
        issues_df (pd.DataFrame): DataFrame containing issue data.

    Returns:
        dict: A summary of issues, including counts by severity and type.
    """
    if issues_df.empty:
        return {"total_issues": 0, "severity_counts": {}, "rule_counts": {}}

    # Count issues by severity
    severity_counts = issues_df['Severity'].value_counts().to_dict()

    # Count issues by rule ID
    rule_counts = issues_df['Rule ID'].value_counts().to_dict()

    print(f"total_issues: {len(issues_df)}")
    print(f"severity_counts: {severity_counts}")
    print(f"rule_counts: {rule_counts}")


def identify_common_patterns(issues):
    """Identify common patterns in the issues.

    Args:
        issues (list): A list of issues, each as a dictionary.

    Returns:
        dict: A summary of common patterns.
    """
    # Example: Identifying the most common file locations for issues
    file_location_counts = Counter(issue['fileLocation'] for issue in issues)
    most_common_locations = file_location_counts.most_common(5)  # Top 5 locations

    return {
        "most_common_locations": most_common_locations
    }

# Other analysis functions can be added as needed
