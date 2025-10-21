"""
String utilities library with click-based formatting.

This module uses Click 7.x API which has breaking changes in 8.x.
"""

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
