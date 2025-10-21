"""
String utilities library with click-based formatting.

This module uses Click 7.x API which has breaking changes in 8.x.
Specifically uses deprecated functions that were removed in Click 8.0.
"""

import click
from click import style, echo
from click.termui import get_terminal_size  # REMOVED in Click 8.0!
from click.utils import get_os_args  # REMOVED in Click 8.0!


def format_text(text, bold=False, fg=None):
    """
    Format text with styling using click.style.

    In Click 7.x, the 'fg' parameter accepts color names directly.
    In Click 8.x, some color handling and parameter validation changed.
    """
    # Using Click 7.x API pattern
    return style(text, bold=bold, fg=fg)


def get_terminal_width():
    """
    Get terminal width using Click 7.x deprecated function.

    Uses click.termui.get_terminal_size() which was REMOVED in Click 8.0.
    Click 8.0+ requires using shutil.get_terminal_size() instead.
    """
    # This function exists in Click 7.x but was removed in 8.0
    width, height = get_terminal_size()
    return width


def get_command_args():
    """
    Get command-line arguments using Click 7.x deprecated function.

    Uses click.utils.get_os_args() which was REMOVED in Click 8.0.
    Click 8.0+ requires using sys.argv[1:] directly instead.
    """
    # This function exists in Click 7.x but was removed in 8.0
    return get_os_args()


def parse_options(args):
    """
    Parse command-line style options into a dictionary.

    This uses click.Context and click.Option in a way that's specific
    to Click 7.x internal APIs.
    """
    options = {}

    # This pattern relies on Click 7.x behavior
    for arg in args:
        if arg.startswith('--'):
            if '=' in arg:
                key, value = arg[2:].split('=', 1)
                options[key] = value
            else:
                options[arg[2:]] = True

    return options


def echo_styled(message, bold=False, fg='green'):
    """
    Echo a styled message to stdout.

    Uses click.echo with styling - behavior changed between versions.
    """
    styled_msg = style(message, bold=bold, fg=fg)
    echo(styled_msg)
    return styled_msg


def create_command_context():
    """
    Create a Click context object.

    This uses Click internal APIs that changed between 7.x and 8.x.
    Specifically, Context initialization and info_name handling changed.
    """
    # This pattern works in Click 7.x but may break in 8.x
    ctx = click.Context(click.Command('dummy'))
    return ctx


# Old-style parameter callback (deprecated in Click 2.0, removed in 8.0)
def old_style_callback(ctx, value):
    """
    Parameter callback using the old 2-arg format.

    This was deprecated since Click 2.0 and removed in Click 8.0.
    Click 8.0+ requires callbacks to accept (ctx, param, value).
    """
    return value.upper() if value else value


@click.command()
@click.option('--name', callback=old_style_callback, help='Name to process')
def process_name_command(name):
    """
    Command using old-style callback.

    The callback parameter uses the deprecated 2-arg format which
    breaks in Click 8.0.
    """
    click.echo(f"Processed: {name}")
    return name
