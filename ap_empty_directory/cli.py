"""Command-line interface for ap-empty-directory."""

import argparse
import sys

from ap_empty_directory.empty import empty_directory

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="ap-empty-directory",
        description="Remove files from a directory and clean up empty subdirectories",
    )
    parser.add_argument(
        "directory",
        help="directory to empty",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="recursively delete files in subdirectories",
    )
    parser.add_argument(
        "--dryrun",
        "-n",
        action="store_true",
        help="show what would be deleted without deleting",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="enable debug output",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="suppress progress output",
    )
    parser.add_argument(
        "--exclude-regex",
        "-e",
        type=str,
        default=None,
        help="regex pattern to exclude files from deletion (matched against filename)",
    )

    args = parser.parse_args()

    try:
        empty_directory(
            directory=args.directory,
            recursive=args.recursive,
            dryrun=args.dryrun,
            debug=args.debug,
            quiet=args.quiet,
            exclude_regex=args.exclude_regex,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()
