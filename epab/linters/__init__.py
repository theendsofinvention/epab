# coding=utf-8
"""
Manages linters
"""

import click

from epab.utils import _info, repo_commit, run_once

from ._pep8 import pep8
from ._isort import isort
from ._flake8 import flake8
from ._pylint import pylint
from ._safety import safety


@run_once
def _lint(ctx: click.Context, auto_commit: bool):
    _info('Running all linters')
    ctx.invoke(pep8)
    ctx.invoke(isort)
    ctx.invoke(flake8)
    ctx.invoke(pylint)
    # ctx.invoke(prospector)
    ctx.invoke(safety)
    if auto_commit:
        msg = 'chg: dev: linting [auto]'
        repo_commit(ctx, msg)


@click.command()
@click.pass_context
@click.option('-c', '--auto-commit', is_flag=True, help='Commit the changes')
def lint(ctx: click.Context, auto_commit: bool):
    """
    Runs all linters
    Args:
        ctx: click context
        auto_commit: whether or not to commit results
    """
    _lint(ctx, auto_commit)
