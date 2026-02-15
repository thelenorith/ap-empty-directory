# ap-empty-directory

[![Test](https://github.com/jewzaam/ap-empty-directory/actions/workflows/test.yml/badge.svg)](https://github.com/jewzaam/ap-empty-directory/actions/workflows/test.yml) [![Coverage](https://github.com/jewzaam/ap-empty-directory/actions/workflows/coverage.yml/badge.svg)](https://github.com/jewzaam/ap-empty-directory/actions/workflows/coverage.yml) [![Lint](https://github.com/jewzaam/ap-empty-directory/actions/workflows/lint.yml/badge.svg)](https://github.com/jewzaam/ap-empty-directory/actions/workflows/lint.yml) [![Format](https://github.com/jewzaam/ap-empty-directory/actions/workflows/format.yml/badge.svg)](https://github.com/jewzaam/ap-empty-directory/actions/workflows/format.yml) [![Type Check](https://github.com/jewzaam/ap-empty-directory/actions/workflows/typecheck.yml/badge.svg)](https://github.com/jewzaam/ap-empty-directory/actions/workflows/typecheck.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Remove files from a directory and clean up empty subdirectories.

## Documentation

This tool is part of the astrophotography pipeline. For comprehensive documentation, see:

- [Pipeline Overview](https://github.com/jewzaam/ap-base/blob/main/docs/index.md) - Introduction to the pipeline architecture
- [Workflow Guide](https://github.com/jewzaam/ap-base/blob/main/docs/workflow.md) - Step-by-step processing workflows
- [Tool API Reference](https://github.com/jewzaam/ap-base/blob/main/docs/tools/ap-empty-directory.md) - Detailed documentation for this tool

## Overview

A tool for clearing out directories by removing all files and optionally cleaning up empty subdirectories. Useful in astrophotography pipelines for resetting working directories between processing runs.

Key features:
- Delete files in a directory (non-recursive by default)
- Optionally recurse into subdirectories with `--recursive`
- Automatically remove empty directories after file deletion
- Dry-run mode to preview changes

## Installation

### Development

```bash
make install-dev
```

### From Git

```bash
pip install git+https://github.com/jewzaam/ap-empty-directory.git
```

## Usage

```bash
# Remove files in top-level directory only
ap-empty-directory /path/to/blink

# Remove all files recursively and clean up empty directories
ap-empty-directory /path/to/blink --recursive

# Preview what would be deleted
ap-empty-directory /path/to/blink --recursive --dryrun
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--recursive` | `-r` | recursively delete files in subdirectories |
| `--dryrun` | `-n` | show what would be deleted without deleting |
| `--debug` | `-d` | enable debug output |
| `--quiet` | `-q` | suppress progress output |
