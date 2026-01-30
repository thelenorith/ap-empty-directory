"""Core functionality for emptying directories."""

import os

from ap_common.filesystem import delete_empty_directories
from ap_common.utils import replace_env_vars


def resolve_path(path: str) -> str:
    """
    Resolve a path by expanding environment variables and user home directory.

    Args:
        path: Path to resolve

    Returns:
        Resolved absolute path
    """
    path = replace_env_vars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path


def _delete_files_in_dir(directory: str, dryrun: bool = False, debug: bool = False):
    """
    Delete all files in a single directory (non-recursive).

    Args:
        directory: Path to the directory
        dryrun: If True, print what would be deleted without actually deleting
        debug: If True, print detailed information about each file
    """
    for entry in os.listdir(directory):
        filepath = os.path.join(directory, entry)
        if os.path.isfile(filepath):
            if debug or dryrun:
                print(f"{'[DRYRUN] ' if dryrun else ''}Deleting file: {filepath}")
            if not dryrun:
                os.remove(filepath)


def delete_files_in_directory(directory: str, recursive: bool = False, dryrun: bool = False, debug: bool = False):
    """
    Delete all files in a directory.

    Args:
        directory: Path to the directory to empty
        recursive: If True, delete files in subdirectories as well
        dryrun: If True, print what would be deleted without actually deleting
        debug: If True, print detailed information about each file
    """
    directory = resolve_path(directory)

    if not os.path.isdir(directory):
        raise ValueError(f"Not a directory: {directory}")

    if debug:
        print(f"delete_files_in_directory({directory}, recursive={recursive}, dryrun={dryrun})")

    if recursive:
        for root, dirs, files in os.walk(directory):
            _delete_files_in_dir(root, dryrun=dryrun, debug=debug)
    else:
        _delete_files_in_dir(directory, dryrun=dryrun, debug=debug)


def empty_directory(directory: str, recursive: bool = False, dryrun: bool = False, debug: bool = False):
    """
    Empty a directory by removing all files and then removing empty subdirectories.

    Args:
        directory: Path to the directory to empty
        recursive: If True, delete files in subdirectories as well
        dryrun: If True, print what would be deleted without actually deleting
        debug: If True, print detailed information about operations
    """
    delete_files_in_directory(directory, recursive=recursive, dryrun=dryrun, debug=debug)

    if recursive:
        delete_empty_directories(directory, dryrun=dryrun)
