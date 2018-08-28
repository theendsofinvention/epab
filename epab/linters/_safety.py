# coding=utf-8
"""
Safety linter
"""

import click
import elib_run

import epab.utils


@epab.utils.run_once
def _safety():
    elib_run.run('safety check --bare', mute=True)


@click.command()
def safety():
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    _safety()
