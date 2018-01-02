# coding=utf-8
"""
Manages output functions
"""

import click


def _sanitize(input_: str) -> str:
    input_ = f'EPAB: {input_}'
    return input_.encode('ascii', 'ignore').decode()


def info(txt: str, **args):
    """
    Prints out informative text

    :param txt: text to print
    :param args: additional arguments to `click.secho` command
    """
    txt = _sanitize(txt)
    click.secho(txt, fg='green', **args)


def error(txt: str, **args):
    """
    Prints out an error

    :param txt: text to print
    :param args: additional arguments to `click.secho` command
    """
    txt = _sanitize(txt)
    click.secho(txt, fg='red', err=True, **args)


def cmd_start(txt: str, **args):
    """
    Prints out the start of a sub-process

    This command should be followed by à call to `cmd_end`

    :param txt: text to print
    :param args: additional arguments to `click.secho` command
    """
    txt = _sanitize(txt)
    click.secho(txt, fg='magenta', nl=False, **args)


def cmd_end(txt: str, **args):
    """
    Prints out the end of a sub-process

    This should follow a call to `cmd_start`

    :param txt: text to print
    :param args: additional arguments to `click.secho` command
    """
    txt = _sanitize(txt).replace('EPAB: ', '')
    click.secho(txt, fg='magenta', **args)


def std_out(process_name: str, txt: str, **args):
    """
    Prints out text from a sub-process standard out stream

    :param process_name: process name
    :param txt: text to print
    :param args: additional arguments to `click.secho` command
    """
    txt = _sanitize(f'{process_name}: {txt}')
    click.secho(txt, fg='cyan', **args)


def std_err(process_name: str, txt: str, **args):
    """
    Prints out text from a sub-process standard error stream

    :param process_name: process name
    :param txt: text to print
    :param args: additional arguments to `click.secho` command
    """
    txt = _sanitize(f'{process_name}: {txt}')
    click.secho(txt, fg='red', **args)
