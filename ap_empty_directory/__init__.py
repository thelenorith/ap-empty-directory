"""ap-empty-directory: CLI tool to empty directories by removing files and empty dirs"""

from ap_empty_directory.empty import (
    delete_files_in_directory,
    empty_directory,
    resolve_path,
)

__version__ = "0.1.0"
__all__ = [
    "delete_files_in_directory",
    "empty_directory",
    "resolve_path",
    "__version__",
]
