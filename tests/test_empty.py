"""Tests for the empty module."""

import os
import tempfile

import pytest

from ap_empty_directory.empty import delete_files_in_directory, empty_directory


class TestDeleteFilesInDirectory:
    """Tests for delete_files_in_directory function."""

    def test_delete_files_non_recursive(self):
        """Test deleting files only in the top-level directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files in top directory
            file1 = os.path.join(tmpdir, "file1.txt")
            file2 = os.path.join(tmpdir, "file2.txt")
            open(file1, "w").close()
            open(file2, "w").close()

            # Create subdirectory with file
            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)
            subfile = os.path.join(subdir, "subfile.txt")
            open(subfile, "w").close()

            # Delete non-recursively
            delete_files_in_directory(tmpdir, recursive=False)

            # Top-level files should be gone
            assert not os.path.exists(file1)
            assert not os.path.exists(file2)
            # Subdir and its file should still exist
            assert os.path.exists(subdir)
            assert os.path.exists(subfile)

    def test_delete_files_recursive(self):
        """Test deleting files recursively."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files in top directory
            file1 = os.path.join(tmpdir, "file1.txt")
            open(file1, "w").close()

            # Create nested subdirectories with files
            subdir1 = os.path.join(tmpdir, "subdir1")
            subdir2 = os.path.join(subdir1, "subdir2")
            os.makedirs(subdir2)
            subfile1 = os.path.join(subdir1, "subfile1.txt")
            subfile2 = os.path.join(subdir2, "subfile2.txt")
            open(subfile1, "w").close()
            open(subfile2, "w").close()

            # Delete recursively
            delete_files_in_directory(tmpdir, recursive=True)

            # All files should be gone
            assert not os.path.exists(file1)
            assert not os.path.exists(subfile1)
            assert not os.path.exists(subfile2)
            # Directories should still exist (empty)
            assert os.path.exists(subdir1)
            assert os.path.exists(subdir2)

    def test_delete_files_dryrun(self):
        """Test dryrun mode doesn't delete anything."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = os.path.join(tmpdir, "file1.txt")
            open(file1, "w").close()

            delete_files_in_directory(tmpdir, recursive=False, dryrun=True)

            # File should still exist
            assert os.path.exists(file1)

    def test_invalid_directory(self):
        """Test that ValueError is raised for non-existent directory."""
        with pytest.raises(ValueError, match="Not a directory"):
            delete_files_in_directory("/nonexistent/path")


class TestEmptyDirectory:
    """Tests for empty_directory function."""

    def test_empty_directory_non_recursive(self):
        """Test emptying directory non-recursively."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file
            file1 = os.path.join(tmpdir, "file1.txt")
            open(file1, "w").close()

            # Create subdirectory with file
            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)
            subfile = os.path.join(subdir, "subfile.txt")
            open(subfile, "w").close()

            empty_directory(tmpdir, recursive=False)

            # Top-level file should be gone
            assert not os.path.exists(file1)
            # Subdir and its contents should still exist
            assert os.path.exists(subdir)
            assert os.path.exists(subfile)

    def test_empty_directory_recursive(self):
        """Test emptying directory recursively removes files and empty dirs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested structure
            subdir1 = os.path.join(tmpdir, "subdir1")
            subdir2 = os.path.join(subdir1, "subdir2")
            os.makedirs(subdir2)

            file1 = os.path.join(tmpdir, "file1.txt")
            subfile1 = os.path.join(subdir1, "subfile1.txt")
            subfile2 = os.path.join(subdir2, "subfile2.txt")
            open(file1, "w").close()
            open(subfile1, "w").close()
            open(subfile2, "w").close()

            empty_directory(tmpdir, recursive=True)

            # All files should be gone
            assert not os.path.exists(file1)
            assert not os.path.exists(subfile1)
            assert not os.path.exists(subfile2)
            # Empty directories should also be removed
            assert not os.path.exists(subdir1)
            assert not os.path.exists(subdir2)
            # Root directory should still exist
            assert os.path.exists(tmpdir)

    def test_empty_directory_dryrun(self):
        """Test dryrun mode doesn't modify anything."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = os.path.join(tmpdir, "file1.txt")
            open(file1, "w").close()

            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)

            empty_directory(tmpdir, recursive=True, dryrun=True)

            # Everything should still exist
            assert os.path.exists(file1)
            assert os.path.exists(subdir)
