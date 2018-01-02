# coding=utf-8
"""
Manages output functions
"""

import click


def _sanitize(input_: str) -> str:
    input_ = f'EPAB: {input_}'
    return input_.encode('ascii', 'ignore').decode()


def info(txt: str, **args):
    txt = _sanitize(txt)
    click.secho(txt, fg='green', **args)


def error(txt: str, **args):
    txt = _sanitize(txt)
    click.secho(txt, fg='red', err=True, **args)


def cmd_start(txt: str, **args):
    txt = _sanitize(txt)
    click.secho(txt, fg='magenta', nl=False, **args)


def cmd_end(txt: str, **args):
    txt = _sanitize(txt).replace('EPAB: ', '')
    click.secho(txt, fg='magenta', **args)


def std_out(txt: str, **args):
    txt = _sanitize(txt)
    click.secho(txt, fg='cyan', **args)
