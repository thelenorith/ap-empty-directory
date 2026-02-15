# Test Plan

> This document describes the testing strategy for this project. It serves as the single source of truth for testing decisions and rationale.

## Overview

<!-- Brief description of what this project does and why testing matters for it -->

**Project:** ap-empty-directory
**Primary functionality:** Remove files from a directory and clean up empty subdirectories

## Testing Philosophy

<!-- What approach does this project take to testing? What's in scope vs out of scope? -->

This project follows the [ap-base Testing Standards](https://github.com/jewzaam/ap-base/blob/main/standards/testing.md).

Key testing principles for this project:

- Test file deletion behavior across recursive and non-recursive modes
- Verify safety features (dryrun, exclude-regex) prevent unintended data loss
- Ensure error handling is robust for permission errors and invalid paths

## Test Categories

### Unit Tests

Tests for isolated functions with mocked dependencies.

| Module | Function | Test Coverage | Notes |
|--------|----------|---------------|-------|
| `empty.py` | `delete_files_in_directory()` | Core deletion logic, recursive/non-recursive, dryrun, exclude patterns | Uses tmp_path fixtures |
| `empty.py` | `empty_directory()` | End-to-end directory emptying with cleanup | Verifies empty dir removal |
| `empty.py` | `_delete_files_in_dir()` | Single-directory file deletion | Tests permission error handling |
| `cli.py` | `main()` | Argument parsing, flag combinations, error handling | Uses monkeypatch for sys.argv |

### Integration Tests

Tests for multiple components working together.

| Workflow | Components | Test Coverage | Notes |
|----------|------------|---------------|-------|
| CLI end-to-end | `cli.py` + `empty.py` | Full CLI execution with real filesystem operations | Tests all flag combinations |
| Recursive cleanup | `empty.py` + `ap_common.filesystem` | File deletion followed by empty directory removal | Verifies directory tree cleanup |

## Untested Areas

<!-- Be explicit about what is NOT tested and why -->

| Area | Reason Not Tested |
|------|-------------------|
| `resolve_path()` environment variable expansion | Covered by ap-common tests |
| `delete_empty_directories()` internals | Provided by ap-common, tested there |

## Bug Fix Testing Protocol

All bug fixes to existing functionality **must** follow TDD:

1. Write a failing test that exposes the bug
2. Verify the test fails before implementing the fix
3. Implement the fix
4. Verify the test passes
5. Verify reverting the fix causes the test to fail again
6. Commit test and fix together with issue reference

### Regression Tests

| Issue | Test | Description |
|-------|------|-------------|
| <!-- #123 --> | `test_function_issue_123` | <!-- what bug was fixed --> |

## Coverage Goals

**Target:** 80%+ line coverage

**Philosophy:** Coverage measures completeness, not quality. A test that executes code without meaningful assertions provides no value. Focus on:

- Testing behavior, not implementation details
- Covering edge cases and error conditions
- Ensuring assertions verify expected outcomes

## Running Tests

```bash
# Run all tests
make test

# Run with coverage
make coverage

# Run specific test
pytest tests/test_module.py::TestClass::test_function
```

## Test Data

<!-- Describe how test data is managed -->

Test data is:
- Generated programmatically in fixtures where possible
- Stored in `tests/fixtures/` when static files are needed
- Documented in `tests/fixtures/README.md`

**No Git LFS** - all test data must be small (< 100KB) or generated.

## Maintenance

<!-- How should tests be maintained over time? -->

When modifying this project:

1. **Adding features**: Add tests for new functionality after implementation
2. **Fixing bugs**: Follow TDD protocol above (test first, then fix)
3. **Refactoring**: Existing tests should pass without modification (behavior unchanged)
4. **Removing features**: Remove associated tests

## Changelog

<!-- Track significant changes to testing strategy -->

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-02-15 | Initial test plan | Project creation |

---
