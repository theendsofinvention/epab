# coding=utf-8
"""
Flake8 linter
"""

import click
import elib_run

import epab.utils
from epab.core import config


@epab.utils.run_once
def _bandit():
    elib_run.run(f'bandit {config.PACKAGE_NAME()} -r', mute=True)


@click.command()
def bandit():
    """
    Runs Flake8 (http://flake8.pycqa.org/en/latest/)
    """
    _bandit()
