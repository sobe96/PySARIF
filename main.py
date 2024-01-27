import file_reader
import data_analysis
import dataframe_manager
import utils

def main():
    file_path = 'data/5.10/svace-res.sarif'
    sarif_data = file_reader.read_sarif_file(file_path)
    data_analysis.summarize_issues(sarif_data)
    issues_df = dataframe_manager.create_issues_dataframe(sarif_data)

    prefixes = [
        "file:///sast/packages-to-analyze/linux-astra-modules-5.10/linux-astra-modules-5.10-5.10.190",
        "file:///"
    ]
    for prefix in prefixes:
        issues_df = utils.remove_specific_prefix(issues_df, 'File Location', prefix)

    print("___________________________________________________________________________________________________________")
    most_common_prefixes = utils.get_common_prefixes(issues_df, 'File Location', 2)
    for prefix, count in most_common_prefixes:
        print(f"Prefix: {prefix}, Count: {count}")

    print("___________________________________________________________________________________________________________")
    # Check if there are any duplicate rows
    utils.check_duplicates(issues_df)

    print("___________________________________________________________________________________________________________")
    utils.save_csv(issues_df)

if __name__ == "__main__":
    main()