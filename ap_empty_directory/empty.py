"""Core functionality for emptying directories."""

import logging
import os
import re

from ap_common.filesystem import delete_empty_directories
from ap_common.utils import replace_env_vars

logger = logging.getLogger(__name__)


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
    directory: str,
    dryrun: bool = False,
    exclude_pattern: re.Pattern | None = None,
) -> list[str]:
    """
    Delete all files in a single directory (non-recursive).

    Args:
        directory: Path to the directory
        dryrun: If True, log what would be deleted without actually deleting
        exclude_pattern: Compiled regex pattern to exclude files from deletion

    Returns:
        List of files that failed to delete (empty if all succeeded)
    """
    failed_files: list[str] = []
    for entry in os.listdir(directory):
        filepath = os.path.join(directory, entry)
        if os.path.isfile(filepath):
            # Check if file matches exclude pattern
            if exclude_pattern and exclude_pattern.search(entry):
                logger.debug(f"Skipping excluded file: {filepath}")
                continue
            if dryrun:
                logger.info(f"[DRYRUN] Deleting file: {filepath}")
            else:
                logger.debug(f"Deleting file: {filepath}")
            if not dryrun:
                try:
                    os.remove(filepath)
                except OSError as e:
                    logger.warning(f"Failed to delete {filepath}: {e}")
                    failed_files.append(filepath)
    return failed_files


def delete_files_in_directory(
    directory: str,
    recursive: bool = False,
    dryrun: bool = False,
    exclude_regex: str | None = None,
) -> list[str]:
    """
    Delete all files in a directory.

    Args:
        directory: Path to the directory to empty
        recursive: If True, delete files in subdirectories as well
        dryrun: If True, log what would be deleted without actually deleting
        exclude_regex: Regex pattern to exclude files from deletion (matched against filename)

    Returns:
        List of files that failed to delete (empty if all succeeded)
    """
    directory = resolve_path(directory)

    if not os.path.isdir(directory):
        raise ValueError(f"Not a directory: {directory}")

    # Compile the exclude regex pattern if provided
    exclude_pattern = None
    if exclude_regex:
        exclude_pattern = re.compile(exclude_regex)

    logger.debug(
        f"delete_files_in_directory({directory}, "
        f"recursive={recursive}, "
        f"dryrun={dryrun}, "
        f"exclude_regex={exclude_regex!r})"
    )

    failed_files: list[str] = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            failed_files.extend(
                _delete_files_in_dir(
                    root,
                    dryrun=dryrun,
                    exclude_pattern=exclude_pattern,
                )
            )
    else:
        failed_files.extend(
            _delete_files_in_dir(
                directory,
                dryrun=dryrun,
                exclude_pattern=exclude_pattern,
            )
        )
    return failed_files


def empty_directory(
    directory: str,
    recursive: bool = False,
    dryrun: bool = False,
    exclude_regex: str | None = None,
) -> list[str]:
    """
    Empty a directory by removing all files and then removing empty subdirectories.

    Args:
        directory: Path to the directory to empty
        recursive: If True, delete files in subdirectories as well
        dryrun: If True, log what would be deleted without actually deleting
        exclude_regex: Regex pattern to exclude files from deletion (matched against filename)

    Returns:
        List of files that failed to delete (empty if all succeeded)
    """
    failed_files = delete_files_in_directory(
        directory,
        recursive=recursive,
        dryrun=dryrun,
        exclude_regex=exclude_regex,
    )

    if recursive:
        try:
            delete_empty_directories(directory, dryrun=dryrun)
        except OSError as e:
            logger.warning(f"Failed to clean up empty directories: {e}")

    return failed_files
