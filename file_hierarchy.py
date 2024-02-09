import pandas as pd
from collections import defaultdict


def build_and_print_hierarchy(df):
    hierarchy = {'_subfolders': {}, '_files': []}  # Root of the hierarchy

    for file_location in df['File Location']:
        path_parts = file_location.split('/')  # Split the file path
        current = hierarchy

        for part in path_parts[:-1]:  # Traverse and build the hierarchy for directories
            if part not in current['_subfolders']:
                current['_subfolders'][part] = {'_subfolders': {}, '_files': []}
            current = current['_subfolders'][part]

        current['_files'].append(path_parts[-1])  # Add the file to the list in the deepest directory

    def print_hierarchy(node, indent=""):
        for folder, content in node['_subfolders'].items():
            print(f"{indent}{folder}/ ({len(content['_files'])})")
            print_hierarchy(content, indent + "    ")

    print_hierarchy(hierarchy)