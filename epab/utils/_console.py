# coding=utf-8
"""
Manages output functions
"""

import click
import io


def _sanitize(input_: str):
    in_stream = input_.encode('utf8')
    return in_stream.decode(errors='replace')


def _info(txt: str, **args):
    txt = _sanitize(txt)
    click.secho(txt, fg='green', **args)


def _error(txt: str, **args):
    txt = _sanitize(txt)
    click.secho(txt, fg='red', err=True, **args)


def _cmd(txt: str, **args):
    txt = _sanitize(txt)
    click.secho(txt, fg='magenta', **args)


def _out(txt: str, **args):
    txt = _sanitize(txt)
    click.secho(txt, fg='cyan', **args)
