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

1. **Click 7.1.2** → Click 8.x has breaking changes:
   - Context initialization API changed
   - Parameter handling modified
   - Command name/info handling restructured
   - When Dependabot updates to 8.x, tests will fail

2. **Requests 2.25.1** → Newer versions have changes:
   - JSON handling differences
   - API behavior modifications

3. **Pytest 6.2.5** → Pytest 7.x/8.x changes:
   - Fixture behavior modifications
   - Assertion introspection changes
   - Deprecated patterns removed

### How Tests Will Fail

The test suite in `tests/test_stringutils.py` specifically relies on:

1. **Click 7.x API patterns**: Tests check for specific Context behavior that changed in Click 8.x
   - `test_context_creation()`: Checks `ctx.command.name` which has different behavior in 8.x
   - `test_context_command_attribute()`: Tests Context internal structure that was reorganized

2. **ANSI code generation**: Tests verify specific ANSI escape sequences from Click's styling that may differ between versions

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

```
FAILED tests/test_stringutils.py::TestCreateCommandContext::test_context_creation
```

The test will fail because Click 8.x changed how Context objects are initialized and how they store command metadata.

## Testing Locally

To verify the current setup works:
```bash
pip install -r requirements.txt
pytest tests/ -v
```

All 11 tests should pass with the pinned versions.

To simulate what Dependabot will break:
```bash
# Update click to latest
pip install click --upgrade
pytest tests/ -v
# Tests will fail!
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
