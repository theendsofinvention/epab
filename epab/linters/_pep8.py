# coding=utf-8
"""
Pep8 linter
"""

import click

from epab.utils import do, run_once


@run_once
def _pep8(ctx):
    do(ctx, ['autopep8', '-r', '--in-place', '--max-line-length', '120', '.'])


@click.command()
@click.pass_context
def pep8(ctx):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    _pep8(ctx)
