# coding=utf-8
"""
iSort linter
"""

import click

from epab.utils import do, run_once


@run_once
def _isort(ctx):
    do(ctx, ['isort', '-rc', '-w', '120', '-s', 'versioneer.py', '.'])


@click.command()
@click.pass_context
def isort(ctx):
    """
    Runs iSort (https://pypi.python.org/pypi/isort)
    """
    _isort(ctx)
