# coding=utf-8
"""
iSort linter
"""

from pathlib import Path

import click
import isort as base_sorter

import epab.core
import epab.utils


@epab.utils.run_once
@epab.utils.stashed
def _isort(amend: bool = False, stage: bool = False):
    settings = {
        'line_ending': '\n',
        'line_length': int(epab.core.CONFIG.lint__line_length),
    }
    for py_file in Path('.').rglob('*.py'):
        # print(type(py_file))
        base_sorter.SortImports(file_path=py_file.absolute(), **settings)

        content = py_file.read_bytes()
        content = content.replace(b'\r\n', b'\n')
        py_file.write_bytes(content)
        # with open(filename, 'rb') as f:
        #     content = f.read()
        #     content = content.replace(windows_line_ending, linux_line_ending)
        #
        # with open(filename, 'wb') as f:
        #     f.write(content)

    if amend:
        epab.core.CTX.repo.amend_commit(append_to_msg='sorting imports [auto]')
    elif stage:
        epab.core.CTX.repo.stage_all()


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
