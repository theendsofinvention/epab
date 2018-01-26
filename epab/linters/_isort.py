# coding=utf-8
"""
iSort linter
"""

import click
import epab.utils
from epab.core import CONFIG, CTX


@epab.utils.run_once
@epab.utils.stashed
def _isort(amend: bool = False):
    epab.utils.run(f'isort -rc -w {CONFIG.lint__line_length} .', mute=True)
    if amend:
        CTX.repo.amend_commit(append_to_msg='sorting imports [auto]')


@click.command()
@click.option('-a', '--amend', is_flag=True, help='Amend last commit with changes')
def isort(amend: bool = False):
    """
    Runs iSort (https://pypi.python.org/pypi/isort)
    """
    _isort(amend)
