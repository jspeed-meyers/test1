"""
Tests for stringutils module.

These tests are written to work with Click 7.1.2 and pytest 6.2.5.
They will break when dependencies are updated by Dependabot due to:
1. Click 8.x API changes (Context, style behavior)
2. Pytest 7.x deprecations and assertion changes
"""

import pytest
from click import Context, Command
from stringutils import (
    format_text,
    parse_options,
    echo_styled,
    create_command_context
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
        assert ctx.info_name == 'dummy'

    def test_context_command_attribute(self):
        """
        Test context command attribute access.

        Click 8.x restructured how Context stores command references.
        """
        ctx = create_command_context()
        assert hasattr(ctx, 'command')
        assert isinstance(ctx.command, Command)


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
