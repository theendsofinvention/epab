# coding=utf-8
"""
iSort linter
"""

import click

import epab.utils
from epab.core import CONFIG, CTX


@epab.utils.run_once
@epab.utils.stashed
def _isort(amend: bool = False, stage: bool = False):
    epab.utils.run(f'isort -rc -w {CONFIG.lint__line_length} .', mute=True)
    if amend:
        CTX.repo.amend_commit(append_to_msg='sorting imports [auto]')
    elif stage:
        CTX.repo.stage_all()


@click.command()
@click.option('-a', '--amend', is_flag=True, help='Amend last commit with changes')
@click.option('-s', '--stage', is_flag=True, help='Stage changed files')
def isort(amend: bool = False, stage: bool = False):
    """
    Runs iSort (https://pypi.python.org/pypi/isort)

    Args:
        amend: whether or not to commit results
        stage: whether or not to stage changes
    """
    _isort(amend, stage)
