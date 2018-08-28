# coding=utf-8
"""
Updates CHANGELOG.rst with the latest commits
"""

import click
import elib_run

import epab.utils
from epab.core import config


@epab.utils.run_once
@epab.utils.stashed
def _compile_qt_resources():
    """
    Compiles PyQT resources file
    """
    if config.QT_RES_SRC():
        epab.utils.ensure_exe('pyrcc5')
        epab.utils.info('Compiling Qt resources')
        elib_run.run(f'pyrcc5 {config.QT_RES_SRC()} -o {config.QT_RES_TGT()}')


@click.command()
def compile_qt_resources():
    """
    Compiles PyQT resources file
    """
    _compile_qt_resources()
