# coding=utf-8
"""
Pylint linter
"""

import sys
from pathlib import Path

import click
import elib_run

import epab.utils
from epab.core import config

IGNORE = '--ignore=CVS'
LINE_LENGTH = f'--max-line-length={config.LINT_LINE_LENGTH()}'
JOBS = '-j 8'
PERSISTENCE = '--persistent=y'
_SITE_PACKAGES = str(Path(sys.executable).parent.parent.joinpath('lib/site-packages')).replace('\\', '/')
_SITE_PACKAGES = _SITE_PACKAGES.replace(':', '')
INIT_HOOK = f'--init-hook="import sys; sys.path.append(\'{_SITE_PACKAGES}\')"'
# noinspection SpellCheckingInspection
DISABLE = "-d disable=logging-format-interpolation,fixme,backtick,long-suffix,raw-checker-failed,bad-inline-option,\
locally-disabled,locally-enabled,suppressed-message,coerce-method,delslice-method,getslice-method,setslice-method,\
next-method-called,too-many-arguments,too-few-public-methods,reload-builtin,oct-method,hex-method,nonzero-method,\
cmp-method,using-cmp-argument,eq-without-hash,exception-message-attribute,sys-max-int,bad-python3-import,\
wrong-import-order,"
EVALUATION = '--evaluation="10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)"'
OUTPUT = '--output-format=text'
SCORE = '--score=n'
BASE_CMD = ' '.join((IGNORE, LINE_LENGTH, JOBS, PERSISTENCE, INIT_HOOK, DISABLE, EVALUATION, OUTPUT, SCORE))


@epab.utils.run_once
def _pylint(src, reports):
    if src is None:
        src = f'./{config.PACKAGE_NAME()}'
    cmd = f'pylint {src}'
    if reports:
        reports = '--reports=y'
    else:
        reports = '--reports=n'
    elib_run.run(f'{cmd} {reports} {BASE_CMD}', mute=True)


@click.command()
@click.argument('src', type=click.Path(exists=True), default=None, required=False)
@click.option('-r', '--reports', is_flag=True, help='Display full report')
def pylint(src, reports):
    """
    Analyze a given python SRC (module or package) with Pylint (SRC must exist)

    Default module: CONFIG['package']
    """
    _pylint(src, reports)
