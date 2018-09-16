# coding=utf-8
"""
Runs all linters
"""
import logging

import click

import epab.utils
from ._bandit import bandit
from ._dead_fixtures import pytest_dead_fixtures
from ._flake8 import flake8
from ._mypy import mypy
# from ._pep8 import pep8
from ._pylint import pylint
from ._safety import safety

# from epab.core import CTX
# from ._sort import sort


LOGGER = logging.getLogger('EPAB')


@epab.utils.run_once
@epab.utils.stashed
def _lint(ctx: click.Context, amend: bool = False, stage: bool = False):
    LOGGER.info('running all linters; stage: %s; amend: %s', stage, amend)
    ctx.invoke(safety)
    ctx.invoke(bandit)
    ctx.invoke(pytest_dead_fixtures)
    # ctx.invoke(pep8, amend=amend, stage=stage)
    ctx.invoke(pylint)
    ctx.invoke(flake8)
    ctx.invoke(mypy)
    # if not CTX.appveyor:
    #     ctx.invoke(sort, amend=amend, stage=stage)


@click.command()
@click.pass_context
@click.option('-a', '--amend', is_flag=True, help='Amend last commit with changes')
@click.option('-s', '--stage', is_flag=True, help='Stage changed files')
def lint(ctx: click.Context, amend: bool = False, stage: bool = False):
    """
    Runs all linters

    Args:
        ctx: click context
        amend: whether or not to commit results
        stage: whether or not to stage changes
    """
    _lint(ctx, amend, stage)
