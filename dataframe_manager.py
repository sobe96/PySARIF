import pandas as pd

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
                "Severity": result.get("level", "Unknown"),
                "Rule ID": result.get("ruleId", "Unknown"),
                "Message": result.get("message", {}).get("text", "No Message"),
                "File Location": result.get("locations", [{}])[0].get("physicalLocation", {}).get("artifactLocation", {}).get(
                    "uri", "Unknown"),
                "Start Line": result.get("locations", [{}])[0].get("physicalLocation", {}).get("region", {}).get(
                    "startLine", -1)
                # Extracting startLine
            }
            issues_list.append(issue)

    return pd.DataFrame(issues_list)


