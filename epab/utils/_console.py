# coding=utf-8
"""
Manages console output functions
"""

import click
import elib_run

from epab.core import CTX, config


class Colors:
    """
    Default text colors
    """
    info = 'green'
    error = 'red'
    cmd = 'magenta'
    stdout = 'cyan'
    stderr = 'red'


def _sanitize(input_: str, prefix=True) -> str:
    if prefix:
        input_ = f'{CTX.prefix}: {input_}'
    return input_.encode('ascii', 'ignore').decode()


def _output(txt, color, **kwargs) -> str:
    if not config.QUIET():
        click.secho(txt, fg=color, **kwargs)
    return txt


def info(txt: str, **kwargs):
    """
    Prints out informative text

    :param txt: text to print
    :param kwargs: additional arguments to `click.secho` command
    """
    txt = _sanitize(txt)
    _output(txt, Colors.info, **kwargs)


def error(txt: str, **kwargs):
    """
    Prints out an error

    :param txt: text to print
    :param kwargs: additional arguments to `click.secho` command
    """
    txt = _sanitize(txt)
    _output(txt, Colors.error, err=True, **kwargs)


def cmd_start(txt: str, **kwargs):
    """
    Prints out the start of a sub-process

    This command should be followed by à call to `cmd_end`

    :param txt: text to print
    :param kwargs: additional arguments to `click.secho` command
    """
    txt = _sanitize(txt)
    _output(txt, Colors.cmd, nl=False, **kwargs)


def cmd_end(txt: str, **kwargs):
    """
    Prints out the end of a sub-process

    This should follow a call to `cmd_start`

    :param txt: text to print
    :param kwargs: additional arguments to `click.secho` command
    """
    txt = _sanitize(txt, prefix=False)
    _output(txt, Colors.cmd, **kwargs)


def std_out(txt: str, **kwargs):
    """
    Prints out text from a sub-process standard out stream

    :param txt: text to print
    :param kwargs: additional arguments to `click.secho` command
    """
    txt = _sanitize(f'{txt}', prefix=False)
    _output(txt, Colors.stdout, nl=True, **kwargs)


def std_err(txt: str, **kwargs):
    """
    Prints out text from a sub-process standard error stream

    :param txt: text to print
    :param kwargs: additional arguments to `click.secho` command
    """
    txt = _sanitize(txt, prefix=False)
    _output(txt, Colors.stderr, err=True, **kwargs)


elib_run.register_hook_cmd_start(cmd_start)
elib_run.register_hook_cmd_end(cmd_end)
elib_run.register_hook_std_out(std_out)
elib_run.register_hook_std_err(std_err)
elib_run.register_hook_info(info)
elib_run.register_hook_error(error)
