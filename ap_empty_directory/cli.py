"""Command-line interface for ap-empty-directory."""

import argparse
import sys

from ap_empty_directory.empty import empty_directory


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="ap-empty-directory",
        description="Empty a directory by removing files and empty subdirectories",
    )
    parser.add_argument(
        "directory",
        help="Path to the directory to empty",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursively delete files in subdirectories",
    )
    parser.add_argument(
        "--dryrun",
        "-n",
        action="store_true",
        help="Print what would be deleted without actually deleting",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Print detailed information about operations",
    )

    args = parser.parse_args()

    try:
        empty_directory(
            directory=args.directory,
            recursive=args.recursive,
            dryrun=args.dryrun,
            debug=args.debug,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
