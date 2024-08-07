def check_path(df):
    loc_col = []
    for file_location in df['File Location']:
        if not file_location.startswith('/'):
            file_location = '/' + file_location
        loc_col.append(file_location)

    df['File Location'] = loc_col
    df = df.drop_duplicates()

    return df


def build_and_print_hierarchy(df):
    hierarchy = {'_subfolders': {}, '_files': []}
    df = check_path(df)


    for file_location in df['File Location']:
        path_parts = [part for part in file_location.replace(':', '/').split('/') if part]  # Avoid empty parts
        current = hierarchy
        for part in path_parts[:-1]:
            current = current.setdefault('_subfolders', {}).setdefault(part, {'_subfolders': {}, '_files': []})
        current['_files'].append(path_parts[-1])

    def print_hierarchy(node, prefix=""):
        children = list(node['_subfolders'].items())
        for i, (name, subnode) in enumerate(children, 1):
            connector = "└── " if i == len(children) else "├── "
            print(f"{prefix}{connector}{name}/ ({len(subnode['_files'])})")
            extension = "    " if i == len(children) else "│   "
            print_hierarchy(subnode, prefix=prefix+extension)
    print_hierarchy(hierarchy)

    return df