# coding=utf-8
"""
iSort linter
"""
from pathlib import Path

import click
import isort

import epab.core
import epab.utils
from epab.core import config


def _fix_newlines(file_path: Path):
    with open(str(file_path)) as stream:
        lines = stream.readlines()
    with open(str(file_path), mode='w', newline='\n') as stream:
        stream.writelines(lines)


def _sort_file(file_path: Path):
    try:
        isort.SortImports(
            file_path=file_path.absolute(),
            known_first_party=config.PACKAGE_NAME(),
            **SETTINGS
        )
        _fix_newlines(file_path)
    except UnicodeDecodeError:  # pragma: no cover
        raise RuntimeError(f'failed to decode file: {file_path}')


SETTINGS = {
    'line_ending': '\n',
    'line_length': int(config.LINT_LINE_LENGTH()),
}


@epab.utils.run_once
@epab.utils.stashed
def _sort(amend: bool = False, stage: bool = False):
    for py_file in Path(f'./{config.PACKAGE_NAME()}').rglob('*.py'):
        _sort_file(py_file.absolute())
    for py_file in Path('./test').rglob('*.py'):
        _sort_file(py_file.absolute())

    if amend:
        epab.core.CTX.repo.amend_commit(append_to_msg='sorting imports [auto]')
    elif stage:
        epab.core.CTX.repo.stage_all()


@click.command()
@click.option('-a', '--amend', is_flag=True, help='Amend last commit with changes')
@click.option('-s', '--stage', is_flag=True, help='Stage changed files')
def sort(amend: bool = False, stage: bool = False):
    """
    Runs iSort (https://pypi.python.org/pypi/isort)

    Args:
        amend: whether or not to commit results
        stage: whether or not to stage changes
    """
    _sort(amend, stage)
