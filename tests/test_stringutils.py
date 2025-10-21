"""
Tests for stringutils module.

These tests are written to work with Click 7.1.2 and pytest 6.2.5.
They will break when dependencies are updated by Dependabot due to:
1. Click 8.x removed deprecated APIs (get_terminal_size, get_os_args)
2. Click 8.x removed old-style parameter callbacks
3. Pytest 7.x deprecations and assertion changes
"""

import pytest
import sys
from click import Context, Command
from click.testing import CliRunner
from stringutils import (
    format_text,
    parse_options,
    echo_styled,
    create_command_context,
    get_terminal_width,
    get_command_args,
    process_name_command,
    old_style_callback
)


class TestFormatText:
    """Test text formatting with Click styling."""

    def test_format_text_bold(self):
        """Test bold text formatting - relies on Click 7.x style behavior."""
        result = format_text("Hello", bold=True)
        # In Click 7.x, this produces ANSI codes in a specific way
        # Click 8.x changed the underlying implementation
        assert "\033[1m" in result  # Bold ANSI code
        assert "Hello" in result

    def test_format_text_color(self):
        """Test colored text - Click 8.x changed color handling."""
        result = format_text("World", fg="red")
        # Click 7.x color codes differ from 8.x
        assert "\033[" in result  # Has ANSI escape codes
        assert "World" in result

    def test_format_text_combined(self):
        """Test combined styling - behavior differs between versions."""
        result = format_text("Test", bold=True, fg="green")
        assert "Test" in result
        assert "\033[" in result


class TestParseOptions:
    """Test option parsing functionality."""

    def test_parse_simple_flag(self):
        """Test parsing simple boolean flags."""
        result = parse_options(["--verbose"])
        assert result == {"verbose": True}

    def test_parse_key_value(self):
        """Test parsing key=value options."""
        result = parse_options(["--output=file.txt"])
        assert result == {"output": "file.txt"}

    def test_parse_multiple_options(self):
        """Test parsing multiple options together."""
        result = parse_options(["--verbose", "--output=test.txt", "--debug"])
        assert result == {
            "verbose": True,
            "output": "test.txt",
            "debug": True
        }


class TestEchoStyled:
    """Test styled echo output."""

    def test_echo_styled_default(self, capsys):
        """Test echo with default styling."""
        result = echo_styled("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_echo_styled_custom(self, capsys):
        """Test echo with custom colors - Click 8.x behavior differs."""
        result = echo_styled("Warning", bold=True, fg="yellow")
        captured = capsys.readouterr()
        assert "Warning" in captured.out


class TestCreateCommandContext:
    """
    Test Click Context creation.

    This is where the main breaking change occurs!
    Click 8.x changed Context initialization and requires different parameters.
    """

    def test_context_creation(self):
        """
        Test creating a Click context.

        In Click 7.x: Context(Command('name')) works fine
        In Click 8.x: Context initialization changed, this pattern breaks
        """
        ctx = create_command_context()
        assert isinstance(ctx, Context)
        # This assertion relies on Click 7.x internals
        # In Click 7.x, info_name may be None by default
        assert ctx.command.name == 'dummy'

    def test_context_command_attribute(self):
        """
        Test context command attribute access.

        Click 8.x restructured how Context stores command references.
        """
        ctx = create_command_context()
        assert hasattr(ctx, 'command')
        assert isinstance(ctx.command, Command)


class TestDeprecatedAPIs:
    """
    Test Click 7.x deprecated APIs that were REMOVED in Click 8.0.

    These tests will FAIL with Click 8.x because the functions no longer exist.
    """

    def test_get_terminal_size(self):
        """
        Test click.termui.get_terminal_size() - REMOVED in Click 8.0.

        Click 7.x: click.termui.get_terminal_size() exists
        Click 8.x: Function removed, must use shutil.get_terminal_size()
        """
        width = get_terminal_width()
        assert isinstance(width, int)
        assert width > 0

    def test_get_os_args(self):
        """
        Test click.utils.get_os_args() - REMOVED in Click 8.0.

        Click 7.x: click.utils.get_os_args() exists
        Click 8.x: Function removed, must use sys.argv[1:] directly
        """
        # This will fail in Click 8.0 with ImportError
        args = get_command_args()
        assert isinstance(args, list)

    def test_old_style_callback_function(self):
        """
        Test old-style parameter callback (2 args) - REMOVED in Click 8.0.

        Click 7.x: Callbacks can accept (ctx, value)
        Click 8.x: Callbacks must accept (ctx, param, value)
        """
        # Test the callback directly
        ctx = create_command_context()
        result = old_style_callback(ctx, "test")
        assert result == "TEST"

    def test_command_with_old_callback(self):
        """
        Test command using old-style callback - BREAKS in Click 8.0.

        The old 2-arg callback format was deprecated in Click 2.0
        and removed in Click 8.0.
        """
        runner = CliRunner()
        # This will work in Click 7.x but fail in 8.0
        result = runner.invoke(process_name_command, ['--name', 'john'])
        # In Click 8.0+, this will fail with TypeError about callback signature
        if result.exit_code != 0:
            print(f"Command failed with exit code {result.exit_code}")
            print(f"Output: {result.output}")
            if result.exception:
                print(f"Exception: {result.exception}")
        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert 'JOHN' in result.output


# Using pytest.fixture decorator in a way that changed between versions
@pytest.fixture
def sample_context():
    """
    Fixture that creates a sample Click context.

    Pytest 7.x changed how fixtures with certain scopes behave.
    """
    return create_command_context()


def test_with_fixture(sample_context):
    """Test using the fixture - may break with pytest version updates."""
    assert sample_context is not None
    assert isinstance(sample_context, Context)
