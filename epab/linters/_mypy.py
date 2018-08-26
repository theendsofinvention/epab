# coding=utf-8
"""
Pep8 linter
"""
import sys

import click

import epab.utils
from epab.core import config


@epab.utils.run_once
@epab.utils.stashed
def _mypy():
    cmd = f'mypy -p {config.PACKAGE_NAME()} --ignore-missing-imports'
    if config.MYPY_ARGS():
        cmd += ' ' + config.MYPY_ARGS()
    _, code = epab.utils.run(cmd, failure_ok=True)
    if code:
        sys.exit(code)


@click.command()
def mypy():
    """
    Runs MyPy type-checker
    """
    _mypy()
