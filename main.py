import json
import pandas as pd
from os.path import commonprefix
from collections import Counter
import os

pd.set_option('display.max_columns', None)

def read_sarif_file(file_path):
    """Read and parse a SARIF file."""
    try:
        with open(file_path, 'r') as file:
            sarif_data = json.load(file)
            return sarif_data
    except Exception as e:
        print(f"Error reading SARIF file: {e}")
        return None

def extract_basic_info(sarif_data):
    """Extract basic information from the SARIF data."""
    if sarif_data:
        runs = sarif_data.get("runs", [])
        print(f"Number of runs: {len(runs)}")
        for i, run in enumerate(runs):
            results = run.get("results", [])
            print(f"Run {i+1} has {len(results)} results")
    else:
        print("No SARIF data to analyze.")

def summarize_issues(sarif_data):
    """Summarize issues found in the SARIF data."""
    if not sarif_data:
        print("No SARIF data to analyze.")
        return

    total_issues = 0
    issues_by_severity = {}
    issues_by_type = {}

    runs = sarif_data.get("runs", [])
    for run in runs:
        results = run.get("results", [])
        total_issues += len(results)
        for result in results:
            severity = result.get("level", "unknown")
            rule_id = result.get("ruleId", "unknown")

            issues_by_severity[severity] = issues_by_severity.get(severity, 0) + 1
            issues_by_type[rule_id] = issues_by_type.get(rule_id, 0) + 1

    print(f"Total Issues: {total_issues}")
    print(f"Issues by Severity: {json.dumps(issues_by_severity, indent=4)}")
    print(f"Issues by Type: {json.dumps(issues_by_type, indent=4)}")

def create_issues_dataframe(sarif_data):
    """Create a DataFrame from issues in the SARIF data."""
    if not sarif_data:
        print("No SARIF data to analyze.")
        return pd.DataFrame()

    issues_list = []
    runs = sarif_data.get("runs", [])
    for run in runs:
        tool = run.get("tool", {}).get("driver", {}).get("name", "Unknown Tool")
        results = run.get("results", [])
        for result in results:
            issue = {
                "Tool": tool,
                "Rule ID": result.get("ruleId", ""),
                "Message": result.get("message", {}).get("text", ""),
                "File Location": result.get("locations", [{}])[0].get("physicalLocation", {}).get("artifactLocation", {}).get(
                    "uri", ""),
                "Start Line": result.get("locations", [{}])[0].get("physicalLocation", {}).get("region", {}).get(
                    "startLine", 0)
                # Extracting startLine
            }
            issues_list.append(issue)

    return pd.DataFrame(issues_list)

def shorten_file_paths(df, file_path_column):
    """Shorten file paths in a DataFrame column."""
    paths = df[file_path_column].tolist()
    common_path = commonprefix(paths)

    # Ensure that the common path ends with a slash to avoid partial directory names
    if not common_path.endswith('/'):
        common_path = common_path.rsplit('/', 1)[0] + '/'

    # Apply the trimming to each path
    df[file_path_column] = df[file_path_column].apply(lambda x: x[len(common_path):])
    return df


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

file_path = 'data/5.10/pvs-report.sarif'  # Replace with your .sarif file path
sarif_data = read_sarif_file(file_path)
extract_basic_info(sarif_data)
summarize_issues(sarif_data)

issues_df = create_issues_dataframe(sarif_data)

prefixes = [
    "file:///sast/packages-to-analyze/linux-astra-modules-5.10/linux-astra-modules-5.10-5.10.190",
    "file:///"
]
for prefix in prefixes:
    issues_df = remove_specific_prefix(issues_df, 'File Location', prefix)

print("______________________________________________________________________________________________________________")
most_common_prefixes = get_common_prefixes(issues_df, 'File Location', 2)
for prefix, count in most_common_prefixes:
    print(f"Prefix: {prefix}, Count: {count}")
#    issues_df = remove_specific_prefix(issues_df, 'File Location', prefix)

print("______________________________________________________________________________________________________________")
# Check if there are any duplicate rows
duplicate_rows = issues_df.duplicated()

# Count the number of duplicate rows
num_duplicates = duplicate_rows.sum()
print(f"Number of duplicate rows: {num_duplicates}")

# Optional: Display the duplicate rows
if num_duplicates > 0:
    print("Duplicate Rows:")
    print(issues_df[duplicate_rows])


print("______________________________________________________________________________________________________________")

print(issues_df.head())
issues_df.to_csv("issues_output.csv", index=False)
