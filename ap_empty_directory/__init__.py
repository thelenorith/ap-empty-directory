"""ap-empty-directory: CLI tool to empty directories by removing files and empty subdirectories."""

from ap_empty_directory.empty import delete_files_in_directory, empty_directory, resolve_path

__all__ = ["delete_files_in_directory", "empty_directory", "resolve_path"]
