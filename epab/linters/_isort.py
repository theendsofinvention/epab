# coding=utf-8
"""
iSort linter
"""

import click
import epab.utils


@epab.utils.run_once
def _isort(ctx):
    epab.utils.do(ctx, ['isort', '-rc', '-w', '120', '-s', 'versioneer.py', '.'])


@click.command()
@click.pass_context
def isort(ctx):
    """
    Runs iSort (https://pypi.python.org/pypi/isort)
    """
    _isort(ctx)
