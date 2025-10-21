"""
String utilities library with click-based formatting.

This module has been updated to work with Click 8.x.
All deprecated APIs have been replaced with standard library equivalents.
"""

import sys
import shutil
import click
from click import style, echo


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
    Get terminal width using shutil (Click 8.0+ compatible).

    In Click 7.x, this used click.termui.get_terminal_size() which was REMOVED in Click 8.0.
    Click 8.0+ requires using shutil.get_terminal_size() instead.
    """
    # Use shutil.get_terminal_size() which is the standard library approach
    terminal_size = shutil.get_terminal_size()
    return terminal_size.columns


def get_command_args():
    """
    Get command-line arguments using sys.argv (Click 8.0+ compatible).

    In Click 7.x, this used click.utils.get_os_args() which was REMOVED in Click 8.0.
    Click 8.0+ requires using sys.argv[1:] directly instead.
    """
    # Use sys.argv[1:] which is the standard library approach
    return sys.argv[1:]


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


# New-style parameter callback (Click 8.0+ compatible)
def old_style_callback(ctx, param, value):
    """
    Parameter callback using the new 3-arg format.

    In Click 7.x, callbacks could use 2-arg format (ctx, value).
    Click 8.0+ requires callbacks to accept (ctx, param, value).
    """
    return value.upper() if value else value


@click.command()
@click.option('--name', callback=old_style_callback, help='Name to process')
def process_name_command(name):
    """
    Command using new-style callback.

    The callback parameter uses the new 3-arg format (ctx, param, value)
    which is required in Click 8.0+.
    """
    click.echo(f"Processed: {name}")
    return name
