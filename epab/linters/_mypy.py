# coding=utf-8
"""
Pep8 linter
"""
import sys

import click

import epab.utils
from epab.core import CONFIG


@epab.utils.run_once
@epab.utils.stashed
def _mypy():
    cmd = f'mypy -p {CONFIG.package} --ignore-missing-imports'
    if CONFIG.mypy__args:
        cmd += ' ' + CONFIG.mypy__args
    epab.utils.add_to_gitignore('.mypy_cache')
    _, code = epab.utils.run(cmd, failure_ok=True)
    if code:
        sys.exit(code)


@click.command()
def mypy():
    """
    Runs MyPy type-checker
    """
    _mypy()
