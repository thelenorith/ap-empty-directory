"""Tests for the empty module."""

import pytest

from ap_empty_directory.empty import delete_files_in_directory, empty_directory


class TestDeleteFilesInDirectory:
    """Tests for delete_files_in_directory function."""

    def test_delete_files_non_recursive(self, tmp_path):
        """Test deleting files only in the top-level directory."""
        # Create files in top directory
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.touch()
        file2.touch()

        # Create subdirectory with file
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        subfile = subdir / "subfile.txt"
        subfile.touch()

        # Delete non-recursively
        delete_files_in_directory(str(tmp_path), recursive=False)

        # Top-level files should be gone
        assert not file1.exists()
        assert not file2.exists()
        # Subdir and its file should still exist
        assert subdir.exists()
        assert subfile.exists()

    def test_delete_files_recursive(self, tmp_path):
        """Test deleting files recursively."""
        # Create files in top directory
        file1 = tmp_path / "file1.txt"
        file1.touch()

        # Create nested subdirectories with files
        subdir1 = tmp_path / "subdir1"
        subdir2 = subdir1 / "subdir2"
        subdir2.mkdir(parents=True)
        subfile1 = subdir1 / "subfile1.txt"
        subfile2 = subdir2 / "subfile2.txt"
        subfile1.touch()
        subfile2.touch()

        # Delete recursively
        delete_files_in_directory(str(tmp_path), recursive=True)

        # All files should be gone
        assert not file1.exists()
        assert not subfile1.exists()
        assert not subfile2.exists()
        # Directories should still exist (empty)
        assert subdir1.exists()
        assert subdir2.exists()

    def test_delete_files_dryrun(self, tmp_path):
        """Test dryrun mode doesn't delete anything."""
        file1 = tmp_path / "file1.txt"
        file1.touch()

        delete_files_in_directory(str(tmp_path), recursive=False, dryrun=True)

        # File should still exist
        assert file1.exists()

    def test_delete_files_invalid_directory(self):
        """Test that ValueError is raised for non-existent directory."""
        with pytest.raises(ValueError, match="Not a directory"):
            delete_files_in_directory("/nonexistent/path")


class TestEmptyDirectory:
    """Tests for empty_directory function."""

    def test_empty_directory_non_recursive(self, tmp_path):
        """Test emptying directory non-recursively."""
        # Create file
        file1 = tmp_path / "file1.txt"
        file1.touch()

        # Create subdirectory with file
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        subfile = subdir / "subfile.txt"
        subfile.touch()

        empty_directory(str(tmp_path), recursive=False)

        # Top-level file should be gone
        assert not file1.exists()
        # Subdir and its contents should still exist
        assert subdir.exists()
        assert subfile.exists()

    def test_empty_directory_recursive(self, tmp_path):
        """Test emptying directory recursively removes files and empty dirs."""
        # Create nested structure
        subdir1 = tmp_path / "subdir1"
        subdir2 = subdir1 / "subdir2"
        subdir2.mkdir(parents=True)

        file1 = tmp_path / "file1.txt"
        subfile1 = subdir1 / "subfile1.txt"
        subfile2 = subdir2 / "subfile2.txt"
        file1.touch()
        subfile1.touch()
        subfile2.touch()

        empty_directory(str(tmp_path), recursive=True)

        # All files should be gone
        assert not file1.exists()
        assert not subfile1.exists()
        assert not subfile2.exists()
        # Empty directories should also be removed
        assert not subdir1.exists()
        assert not subdir2.exists()
        # Root directory should still exist
        assert tmp_path.exists()

    def test_empty_directory_dryrun(self, tmp_path):
        """Test dryrun mode doesn't modify anything."""
        file1 = tmp_path / "file1.txt"
        file1.touch()

        subdir = tmp_path / "subdir"
        subdir.mkdir()

        empty_directory(str(tmp_path), recursive=True, dryrun=True)

        # Everything should still exist
        assert file1.exists()
        assert subdir.exists()
