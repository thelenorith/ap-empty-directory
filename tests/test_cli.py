"""Tests for the CLI module."""

import sys

import pytest

from ap_empty_directory.cli import EXIT_ERROR, EXIT_SUCCESS, main


class TestCLIArgumentParsing:
    """Tests for CLI argument parsing and execution."""

    def test_cli_basic_execution(self, tmp_path, monkeypatch):
        """Test basic CLI execution with valid directory."""
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.touch()

        monkeypatch.setattr(sys, "argv", ["ap-empty-directory", str(tmp_path)])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_SUCCESS
        assert not test_file.exists()

    def test_cli_recursive_flag(self, tmp_path, monkeypatch):
        """Test CLI with --recursive flag."""
        # Create nested structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        file1 = tmp_path / "file1.txt"
        file2 = subdir / "file2.txt"
        file1.touch()
        file2.touch()

        monkeypatch.setattr(
            sys, "argv", ["ap-empty-directory", str(tmp_path), "--recursive"]
        )

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_SUCCESS
        assert not file1.exists()
        assert not file2.exists()
        assert not subdir.exists()  # Should be removed as empty

    def test_cli_recursive_short_flag(self, tmp_path, monkeypatch):
        """Test CLI with -r short flag."""
        file1 = tmp_path / "file1.txt"
        file1.touch()

        monkeypatch.setattr(sys, "argv", ["ap-empty-directory", str(tmp_path), "-r"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_SUCCESS
        assert not file1.exists()

    def test_cli_dryrun_flag(self, tmp_path, monkeypatch, capsys):
        """Test CLI with --dryrun flag doesn't delete files."""
        test_file = tmp_path / "test.txt"
        test_file.touch()

        monkeypatch.setattr(
            sys, "argv", ["ap-empty-directory", str(tmp_path), "--dryrun"]
        )

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_SUCCESS
        assert test_file.exists()  # File should still exist
        captured = capsys.readouterr()
        assert "[DRYRUN]" in captured.out

    def test_cli_dryrun_short_flag(self, tmp_path, monkeypatch):
        """Test CLI with -n short flag."""
        test_file = tmp_path / "test.txt"
        test_file.touch()

        monkeypatch.setattr(sys, "argv", ["ap-empty-directory", str(tmp_path), "-n"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_SUCCESS
        assert test_file.exists()

    def test_cli_debug_flag(self, tmp_path, monkeypatch, capsys):
        """Test CLI with --debug flag produces debug output."""
        test_file = tmp_path / "test.txt"
        test_file.touch()

        monkeypatch.setattr(
            sys, "argv", ["ap-empty-directory", str(tmp_path), "--debug"]
        )

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_SUCCESS
        captured = capsys.readouterr()
        assert "delete_files_in_directory" in captured.out

    def test_cli_debug_short_flag(self, tmp_path, monkeypatch, capsys):
        """Test CLI with -d short flag."""
        test_file = tmp_path / "test.txt"
        test_file.touch()

        monkeypatch.setattr(sys, "argv", ["ap-empty-directory", str(tmp_path), "-d"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_SUCCESS
        captured = capsys.readouterr()
        assert "delete_files_in_directory" in captured.out

    def test_cli_combined_flags(self, tmp_path, monkeypatch, capsys):
        """Test CLI with multiple flags combined."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        file1 = tmp_path / "file1.txt"
        file2 = subdir / "file2.txt"
        file1.touch()
        file2.touch()

        monkeypatch.setattr(
            sys, "argv", ["ap-empty-directory", str(tmp_path), "-r", "-n", "-d"]
        )

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_SUCCESS
        # Files should still exist (dryrun)
        assert file1.exists()
        assert file2.exists()
        # Should have debug output
        captured = capsys.readouterr()
        assert "delete_files_in_directory" in captured.out
        assert "[DRYRUN]" in captured.out


class TestCLIErrorHandling:
    """Tests for CLI error handling."""

    def test_cli_invalid_directory(self, monkeypatch, capsys):
        """Test CLI with non-existent directory exits with error."""
        monkeypatch.setattr(
            sys, "argv", ["ap-empty-directory", "/nonexistent/path/xyz"]
        )

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_ERROR
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "Not a directory" in captured.err

    def test_cli_file_instead_of_directory(self, tmp_path, monkeypatch, capsys):
        """Test CLI with file path instead of directory."""
        test_file = tmp_path / "test.txt"
        test_file.touch()

        monkeypatch.setattr(sys, "argv", ["ap-empty-directory", str(test_file)])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_ERROR
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "Not a directory" in captured.err

    def test_cli_unexpected_error_handling(self, tmp_path, monkeypatch, capsys):
        """Test CLI handles unexpected errors gracefully."""
        # Patch empty_directory to raise an unexpected exception
        from ap_empty_directory import cli

        original_empty_directory = cli.empty_directory

        def mock_empty_directory(*args, **kwargs):
            raise RuntimeError("Unexpected error for testing")

        monkeypatch.setattr(cli, "empty_directory", mock_empty_directory)
        monkeypatch.setattr(sys, "argv", ["ap-empty-directory", str(tmp_path)])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == EXIT_ERROR
        captured = capsys.readouterr()
        assert "Unexpected error:" in captured.err
        assert "Unexpected error for testing" in captured.err

        # Restore original function
        monkeypatch.setattr(cli, "empty_directory", original_empty_directory)
