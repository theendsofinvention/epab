# coding=utf-8
"""
Pep8 linter
"""

import click
import elib_run

import epab.utils
from epab.core import CTX, config


@epab.utils.run_once
@epab.utils.stashed
def _pep8(amend: bool = False, stage: bool = False):
    elib_run.run(
        f'autopep8 -r --in-place --max-line-length {config.LINT_LINE_LENGTH()} {config.PACKAGE_NAME()}',
        mute=True
    )
    elib_run.run(f'autopep8 -r --in-place --max-line-length {config.LINT_LINE_LENGTH()} test', mute=True)
    if amend:
        CTX.repo.amend_commit(append_to_msg='pep8 [auto]')
    elif stage:
        CTX.repo.stage_all()


@click.command()
@click.option('-a', '--amend', is_flag=True, help='Amend last commit with changes')
@click.option('-s', '--stage', is_flag=True, help='Stage changed files')
def pep8(amend: bool = False, stage: bool = False):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)

    Args:
        amend: whether or not to commit results
        stage: whether or not to stage changes
    """
    _pep8(amend, stage)
