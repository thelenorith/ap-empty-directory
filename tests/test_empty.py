"""Tests for the empty module."""

from unittest.mock import patch

import pytest

from ap_empty_directory.empty import (
    _delete_files_in_dir,
    delete_files_in_directory,
    empty_directory,
)


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

    def test_delete_files_debug_output(self, tmp_path, capsys):
        """Test that debug mode produces expected output."""
        file1 = tmp_path / "file1.txt"
        file1.touch()

        delete_files_in_directory(str(tmp_path), recursive=False, debug=True)

        captured = capsys.readouterr()
        assert "delete_files_in_directory" in captured.out
        assert f"recursive={False}" in captured.out
        assert f"dryrun={False}" in captured.out


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


class TestExcludeRegex:
    """Tests for exclude_regex functionality."""

    def test_exclude_single_file(self, tmp_path):
        """Test excluding a specific file from deletion."""
        file1 = tmp_path / "file1.txt"
        keep_file = tmp_path / ".keep"
        file1.touch()
        keep_file.touch()

        delete_files_in_directory(str(tmp_path), exclude_regex=r"\.keep$")

        assert not file1.exists()
        assert keep_file.exists()

    def test_exclude_pattern_matches_multiple_files(self, tmp_path):
        """Test excluding multiple files matching a pattern."""
        file1 = tmp_path / "data.txt"
        keep1 = tmp_path / ".keep"
        keep2 = tmp_path / "dir.keep"
        file1.touch()
        keep1.touch()
        keep2.touch()

        delete_files_in_directory(str(tmp_path), exclude_regex=r"\.keep$")

        assert not file1.exists()
        assert keep1.exists()
        assert keep2.exists()

    def test_exclude_recursive(self, tmp_path):
        """Test exclude pattern works recursively."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        file1 = tmp_path / "file1.txt"
        keep1 = tmp_path / ".keep"
        file2 = subdir / "file2.txt"
        keep2 = subdir / ".keep"
        file1.touch()
        keep1.touch()
        file2.touch()
        keep2.touch()

        delete_files_in_directory(
            str(tmp_path), recursive=True, exclude_regex=r"\.keep$"
        )

        assert not file1.exists()
        assert keep1.exists()
        assert not file2.exists()
        assert keep2.exists()

    def test_exclude_with_empty_directory_cleanup(self, tmp_path):
        """Test that directories with only excluded files are not deleted."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        file1 = tmp_path / "file1.txt"
        keep_file = subdir / ".keep"
        file1.touch()
        keep_file.touch()

        empty_directory(str(tmp_path), recursive=True, exclude_regex=r"\.keep$")

        assert not file1.exists()
        assert subdir.exists()  # Should still exist because .keep is there
        assert keep_file.exists()

    def test_exclude_debug_output(self, tmp_path, capsys):
        """Test that debug mode shows skipped files."""
        keep_file = tmp_path / ".keep"
        keep_file.touch()

        delete_files_in_directory(str(tmp_path), debug=True, exclude_regex=r"\.keep$")

        captured = capsys.readouterr()
        assert "Skipping excluded file" in captured.out
        assert ".keep" in captured.out

    def test_exclude_dryrun(self, tmp_path, capsys):
        """Test exclude pattern with dryrun mode."""
        file1 = tmp_path / "file1.txt"
        keep_file = tmp_path / ".keep"
        file1.touch()
        keep_file.touch()

        delete_files_in_directory(str(tmp_path), dryrun=True, exclude_regex=r"\.keep$")

        captured = capsys.readouterr()
        # file1.txt should be mentioned as would be deleted
        assert "file1.txt" in captured.out
        # Both files should still exist
        assert file1.exists()
        assert keep_file.exists()

    def test_exclude_regex_case_sensitive(self, tmp_path):
        """Test that exclude regex is case sensitive by default."""
        keep_lower = tmp_path / ".keep"
        keep_upper = tmp_path / ".KEEP"
        keep_lower.touch()
        keep_upper.touch()

        delete_files_in_directory(str(tmp_path), exclude_regex=r"\.keep$")

        assert keep_lower.exists()
        assert not keep_upper.exists()

    def test_no_exclude_regex(self, tmp_path):
        """Test that all files are deleted when no exclude_regex is provided."""
        file1 = tmp_path / "file1.txt"
        keep_file = tmp_path / ".keep"
        file1.touch()
        keep_file.touch()

        delete_files_in_directory(str(tmp_path))

        assert not file1.exists()
        assert not keep_file.exists()


class TestErrorHandling:
    """Tests for error handling during file deletion."""

    def test_delete_files_handles_permission_error(self, tmp_path, capsys):
        """Test that permission errors are caught and reported."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.touch()
        file2.touch()

        # Mock os.remove to fail on first file, succeed on second
        original_remove = __builtins__["__import__"]("os").remove
        call_count = 0

        def mock_remove(path):
            nonlocal call_count
            call_count += 1
            if "file1.txt" in str(path):
                raise PermissionError("Permission denied")
            original_remove(path)

        with patch("os.remove", side_effect=mock_remove):
            failed = _delete_files_in_dir(str(tmp_path))

        # Should report the failure
        captured = capsys.readouterr()
        assert "Warning: Failed to delete" in captured.out
        assert "file1.txt" in captured.out
        assert len(failed) == 1
        assert "file1.txt" in failed[0]

    def test_delete_files_continues_after_error(self, tmp_path):
        """Test that deletion continues after encountering an error."""
        import os

        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file3 = tmp_path / "file3.txt"
        file1.touch()
        file2.touch()
        file3.touch()

        original_remove = os.remove

        # Mock os.remove to fail only on file2
        def mock_remove(path):
            if "file2.txt" in str(path):
                raise PermissionError("Permission denied")
            original_remove(path)

        with patch("os.remove", side_effect=mock_remove):
            failed = delete_files_in_directory(str(tmp_path))

        # file2 should be in failed list
        assert len(failed) == 1
        assert "file2.txt" in failed[0]

    def test_delete_files_returns_empty_on_success(self, tmp_path):
        """Test that an empty list is returned when all deletions succeed."""
        file1 = tmp_path / "file1.txt"
        file1.touch()

        failed = delete_files_in_directory(str(tmp_path))

        assert failed == []
        assert not file1.exists()

    def test_empty_directory_returns_failed_files(self, tmp_path):
        """Test that empty_directory returns failed files."""
        file1 = tmp_path / "file1.txt"
        file1.touch()

        def mock_remove(path):
            raise PermissionError("Permission denied")

        with patch("os.remove", side_effect=mock_remove):
            failed = empty_directory(str(tmp_path))

        assert len(failed) == 1
        assert "file1.txt" in failed[0]

    def test_empty_directory_handles_cleanup_error(self, tmp_path, capsys):
        """Test that delete_empty_directories errors are caught."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        with patch(
            "ap_empty_directory.empty.delete_empty_directories",
            side_effect=OSError("Failed to remove directory"),
        ):
            failed = empty_directory(str(tmp_path), recursive=True)

        captured = capsys.readouterr()
        assert "Warning: Failed to clean up empty directories" in captured.out
        assert failed == []
