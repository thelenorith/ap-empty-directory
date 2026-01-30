# ap-empty-directory

CLI tool to empty directories by removing files and empty subdirectories.

## Installation

```bash
pip install git+https://github.com/jewzaam/ap-empty-directory.git
```

For development:

```bash
git clone https://github.com/jewzaam/ap-empty-directory.git
cd ap-empty-directory
make install-dev
```

## Usage

```bash
# Remove files in a directory (non-recursive)
ap-empty-directory /path/to/directory

# Remove files recursively and clean up empty directories
ap-empty-directory /path/to/directory --recursive

# Dry run to see what would be deleted
ap-empty-directory /path/to/directory --recursive --dryrun

# Debug mode for detailed output
ap-empty-directory /path/to/directory --recursive --debug
```

### Options

- `--recursive`, `-r`: Recursively delete files in subdirectories and remove empty directories
- `--dryrun`, `-n`: Print what would be deleted without actually deleting
- `--debug`, `-d`: Print detailed information about operations

## Python API

```python
from ap_empty_directory import empty_directory, delete_files_in_directory

# Empty a directory (delete files and empty subdirs)
empty_directory("/path/to/directory", recursive=True)

# Just delete files (keep directory structure)
delete_files_in_directory("/path/to/directory", recursive=True)
```

## Development

```bash
# Install dev dependencies
make install-dev

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run tests with coverage
make coverage
```

## License

Apache-2.0
