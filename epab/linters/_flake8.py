# coding=utf-8
"""
Flake8 linter
"""

import click
import elib_run

import epab.utils
from epab.core import config

IGNORE = '--ignore=D203,E126'
MAX_LINE_LENGTH = f'--max-line-length={config.LINT_LINE_LENGTH()}'
BASE_EXCLUDE = ".svn,CVS,.bzr,.hg,.git,__pycache__,.tox,__init__.py,build,dist,output,.cache," \
               ".hypothesis,./test/*,./.eggs/*,./.venv"
EXCLUDE = '--exclude ' + BASE_EXCLUDE
MAX_COMPLEXITY = '--max-complexity=10'


@epab.utils.run_once
def _flake8():
    exclude = EXCLUDE + config.FLAKE8_EXCLUDE()
    base_cmd = ' '.join((IGNORE, MAX_LINE_LENGTH, exclude, MAX_COMPLEXITY))
    elib_run.run(f'flake8 {base_cmd}', mute=True)


@click.command()
def flake8():
    """
    Runs Flake8 (http://flake8.pycqa.org/en/latest/)
    """
    _flake8()
