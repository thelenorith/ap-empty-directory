"""Core functionality for emptying directories."""

import os

from ap_common.filesystem import delete_empty_directories


def delete_files_in_directory(directory: str, recursive: bool = False, dryrun: bool = False, debug: bool = False):
    """
    Delete all files in a directory.

    Args:
        directory: Path to the directory to empty
        recursive: If True, delete files in subdirectories as well
        dryrun: If True, print what would be deleted without actually deleting
        debug: If True, print detailed information about each file
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Not a directory: {directory}")

    if debug:
        print(f"delete_files_in_directory({directory}, recursive={recursive}, dryrun={dryrun})")

    if recursive:
        # Walk the directory tree and delete all files
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                if debug or dryrun:
                    print(f"{'[DRYRUN] ' if dryrun else ''}Deleting file: {filepath}")
                if not dryrun:
                    os.remove(filepath)
    else:
        # Only delete files in the top-level directory
        for entry in os.listdir(directory):
            filepath = os.path.join(directory, entry)
            if os.path.isfile(filepath):
                if debug or dryrun:
                    print(f"{'[DRYRUN] ' if dryrun else ''}Deleting file: {filepath}")
                if not dryrun:
                    os.remove(filepath)


def empty_directory(directory: str, recursive: bool = False, dryrun: bool = False, debug: bool = False):
    """
    Empty a directory by removing all files and then removing empty subdirectories.

    Args:
        directory: Path to the directory to empty
        recursive: If True, delete files in subdirectories as well
        dryrun: If True, print what would be deleted without actually deleting
        debug: If True, print detailed information about operations
    """
    # First, delete files
    delete_files_in_directory(directory, recursive=recursive, dryrun=dryrun, debug=debug)

    # Then, delete empty directories (uses ap-common functionality)
    if recursive:
        delete_empty_directories(directory, dryrun=dryrun)
