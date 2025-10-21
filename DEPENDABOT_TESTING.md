# Dependabot Testing Project

This project is intentionally configured to demonstrate Dependabot PRs that will fail due to breaking API changes between dependency versions.

## Project Overview

This is a simple Python utility library with:
- String formatting utilities using Click
- Command-line option parsing
- Comprehensive test suite

## Intentional Breaking Points

### Dependencies with Pinned Versions

The project uses **old pinned versions** with known breaking changes:

1. **Click 7.1.2** → Click 8.x has **real breaking changes**:
   - **Click 8.0+**: Old-style parameter callbacks (2-arg) removed - must use 3-arg format (ctx, param, value)
   - **Click 8.1+**: `get_terminal_size()` removed from `click.termui` - must use `shutil.get_terminal_size()`
   - **Click 8.1+**: `get_os_args()` removed from `click.utils` - must use `sys.argv[1:]`
   - When Dependabot updates to 8.x, tests will fail with ImportError or TypeError

2. **Requests 2.25.1** → Newer versions have changes:
   - JSON handling differences
   - API behavior modifications

3. **Pytest 6.2.5** → Pytest 7.x/8.x changes:
   - Fixture behavior modifications
   - Assertion introspection changes
   - Deprecated patterns removed

### How Tests Will Fail

The test suite in `tests/test_stringutils.py` specifically relies on Click 7.x deprecated APIs:

1. **Click 7.x deprecated functions** (removed in 8.1):
   - `test_get_terminal_size()`: Uses `click.termui.get_terminal_size()`
   - `test_get_os_args()`: Uses `click.utils.get_os_args()`
   - These will fail with `ImportError` in Click 8.1+

2. **Old-style parameter callbacks** (removed in 8.0):
   - `test_command_with_old_callback()`: Uses 2-arg callback format `callback(ctx, value)`
   - Click 8.0+ requires 3-arg format: `callback(ctx, param, value)`
   - Will fail with `TypeError: takes 2 positional arguments but 3 were given`

3. **Fixture patterns**: Uses pytest fixtures in ways that changed between pytest 6.x and 7.x

## Dependabot Configuration

Located at `.github/dependabot.yml`:
- Checks for updates **daily**
- Monitors pip dependencies
- Will create separate PRs for each dependency update
- Each PR will trigger test failures due to API incompatibilities

## Expected Behavior

When Dependabot runs, it will:

1. **Detect available updates** for click, requests, and pytest
2. **Create individual PRs** to update each dependency
3. **Tests will fail** because:
   - Code uses old API patterns
   - Tests explicitly check for version-specific behavior
   - Breaking changes prevent backward compatibility

### Example: Click Update PR

When Dependabot tries to update `click==7.1.2` to `click>=8.0.0`:

**With Click 8.0.0:**
```
FAILED tests/test_stringutils.py::TestDeprecatedAPIs::test_command_with_old_callback
TypeError: old_style_callback() takes 2 positional arguments but 3 were given
```

**With Click 8.1.0+:**
```
ImportError: cannot import name 'get_terminal_size' from 'click.termui'
ImportError: cannot import name 'get_os_args' from 'click.utils'
```

## Testing Locally

To verify the current setup works:
```bash
pip install -r requirements.txt
pytest tests/ -v
```

All 15 tests should pass with the pinned versions.

To simulate what Dependabot will break:
```bash
# Test with Click 8.0.0 (callback breaks)
pip install click==8.0.0
pytest tests/ -v
# 1 test fails with TypeError

# Test with Click 8.1.0+ (imports break)
pip install click==8.1.0
pytest tests/ -v
# Tests fail to import with ImportError
```

## Purpose

This project demonstrates:
- How pinned dependencies can cause issues with automated updates
- Why version compatibility testing is important
- The challenges of maintaining dependencies with breaking changes
- How Dependabot PRs can fail without proper CI/CD guardrails

## Resolution Strategies

When Dependabot PRs fail, typical resolutions include:
1. Update code to use new API patterns
2. Update tests to work with new versions
3. Pin to compatible version ranges
4. Use compatibility shims/adapters
