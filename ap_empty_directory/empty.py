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


def _delete_files_in_dir(
    directory: str, dryrun: bool = False, debug: bool = False
) -> list[str]:
    """
    Delete all files in a single directory (non-recursive).

    Args:
        directory: Path to the directory
        dryrun: If True, print what would be deleted without actually deleting
        debug: If True, print detailed information about each file

    Returns:
        List of files that failed to delete (empty if all succeeded)
    """
    failed_files: list[str] = []
    for entry in os.listdir(directory):
        filepath = os.path.join(directory, entry)
        if os.path.isfile(filepath):
            if debug or dryrun:
                print(f"{'[DRYRUN] ' if dryrun else ''}Deleting file: {filepath}")
            if not dryrun:
                try:
                    os.remove(filepath)
                except OSError as e:
                    print(f"Warning: Failed to delete {filepath}: {e}")
                    failed_files.append(filepath)
    return failed_files


def delete_files_in_directory(
    directory: str, recursive: bool = False, dryrun: bool = False, debug: bool = False
) -> list[str]:
    """
    Delete all files in a directory.

    Args:
        directory: Path to the directory to empty
        recursive: If True, delete files in subdirectories as well
        dryrun: If True, print what would be deleted without actually deleting
        debug: If True, print detailed information about each file

    Returns:
        List of files that failed to delete (empty if all succeeded)
    """
    directory = resolve_path(directory)

    if not os.path.isdir(directory):
        raise ValueError(f"Not a directory: {directory}")

    if debug:
        print(
            f"delete_files_in_directory({directory}, "
            f"recursive={recursive}, "
            f"dryrun={dryrun})"
        )

    failed_files: list[str] = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            failed_files.extend(_delete_files_in_dir(root, dryrun=dryrun, debug=debug))
    else:
        failed_files.extend(_delete_files_in_dir(directory, dryrun=dryrun, debug=debug))
    return failed_files


def empty_directory(
    directory: str, recursive: bool = False, dryrun: bool = False, debug: bool = False
) -> list[str]:
    """
    Empty a directory by removing all files and then removing empty subdirectories.

    Args:
        directory: Path to the directory to empty
        recursive: If True, delete files in subdirectories as well
        dryrun: If True, print what would be deleted without actually deleting
        debug: If True, print detailed information about operations

    Returns:
        List of files that failed to delete (empty if all succeeded)
    """
    failed_files = delete_files_in_directory(
        directory, recursive=recursive, dryrun=dryrun, debug=debug
    )

    if recursive:
        try:
            delete_empty_directories(directory, dryrun=dryrun)
        except OSError as e:
            print(f"Warning: Failed to clean up empty directories: {e}")

    return failed_files
