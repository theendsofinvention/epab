# coding=utf-8
"""
Pep8 linter
"""

import click

import epab.utils
from epab.core import CONFIG, CTX


@epab.utils.run_once
@epab.utils.stashed
def _pep8(amend: bool = False):
    epab.utils.run(f'autopep8 -r --in-place --max-line-length {CONFIG.lint__line_length} .', mute=True)
    if amend:
        CTX.repo.amend_commit(append_to_msg='pep8 [auto]')


@click.command()
@click.option('-a', '--amend', is_flag=True, help='Amend last commit with changes')
def pep8(amend: bool):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    _pep8(amend)
