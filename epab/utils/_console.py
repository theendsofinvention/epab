# coding=utf-8

import click


def _info(txt: str, **args):
    click.secho(txt, fg='green', **args)


def _error(txt: str, **args):
    click.secho(txt, fg='red', err=True, **args)


def _cmd(txt: str, **args):
    click.secho(txt, fg='magenta', **args)


def _out(txt: str, **args):
    click.secho(txt, fg='cyan', **args)
