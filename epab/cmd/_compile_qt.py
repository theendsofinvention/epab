# coding=utf-8
"""
Compiles PyQT file
"""

import logging

import click
import elib_run

import epab.utils
from epab.core import config

LOGGER = logging.getLogger('EPAB')


@epab.utils.run_once
@epab.utils.stashed
@epab.utils.timeit
def _compile_qt_resources():
    """
    Compiles PyQT resources file
    """
    if config.QT_RES_SRC():
        epab.utils.ensure_exe('pyrcc5')
        LOGGER.info('compiling Qt resources')
        elib_run.run(f'pyrcc5 {config.QT_RES_SRC()} -o {config.QT_RES_TGT()}')


@click.command()
def compile_qt_resources():
    """
    Compiles PyQT resources file
    """
    _compile_qt_resources()
