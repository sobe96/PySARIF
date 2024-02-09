import pandas as pd


def create_sarif_dataframe(sarif_data):
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
                "Severity": result.get("level", "Unspecified"),
                "Rule ID": result.get("ruleId", "Unknown"),
                "Message": result.get("message", {}).get("text", "No Message"),
                "File Location": result.get("locations", [{}])[0].get("physicalLocation", {}).get("artifactLocation",
                                                                                                  {}).get(
                    "uri", "Unknown"),
                "Start Line": result.get("locations", [{}])[0].get("physicalLocation", {}).get("region", {}).get(
                    "startLine", -1)
                # Extracting startLine
            }
            issues_list.append(issue)

    return pd.DataFrame(issues_list)


def create_csv_dataframe(csv_df):
    """Process a DataFrame from issues in the CSV data."""
    csv_df.rename(columns={'severity': 'Severity',
                           'warnClass': 'Rule ID',
                           'msg': 'Message',
                           'file': 'File Location',
                           'line': 'Start Line'},
                  inplace=True)

    csv_df['Tool'] = 'Svace'
    csv_df = csv_df[['Tool', 'Severity', 'Rule ID', 'Message', 'File Location', 'Start Line']]

    return csv_df
