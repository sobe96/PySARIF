import file_hierarchy
import utils
def remove_prefix_and_parents(df, prefix):
    """
    Remove a prefix and all its parent directories from a path.

    Args:
        path (str): The original file path.
        prefix (str): The prefix to be removed along with its parents.

    Returns:
        str: The trimmed file path.
    """
    for file_location in df['File Location']:
        if prefix in file_location:
            # Split the path and prefix into segments
            path_segments = file_location.split('/')
            prefix_segments = prefix.split('/')

            # Find the index of the prefix's last segment in the path
            try:
                index = path_segments.index(prefix_segments[-1])
                df = utils.remove_specific_prefix(df, 'File Location', '/'.join(path_segments[:index]))
                # Return the part of the path after the prefix
                return df
            except ValueError:
                # If the prefix's last segment is not found, return the original path
                return df
    return df


def manual_trim_paths(df, filename):
    """
    Iteratively ask the user for prefixes to trim from the paths, including parents.

    Args:
        paths (list of str): The original list of file paths.

    Returns:
        list of str: The list of trimmed file paths.
    """
    while True:
        print(f"\nCurrent path structure of {filename}:")
        file_hierarchy.build_and_print_hierarchy(df)

        # Ask the user for the prefix to trim
        prefix_to_trim = input(
            f"\nEnter the prefix to trim along with all its parents (leave empty and press enter when done) from {filename}: ").strip()
        if not prefix_to_trim:
            break  # Exit the loop if the user is done trimming
        #df = utils.remove_specific_prefix(df, 'File Location', prefix_to_trim)
        # Apply the trimming
        df = remove_prefix_and_parents(df, prefix_to_trim)

    print(f"\nFinal trimmed path structure of {filename}:")
    file_hierarchy.build_and_print_hierarchy(df)

    return df