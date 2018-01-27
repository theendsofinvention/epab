# coding=utf-8
"""
Safety linter
"""

import click

import epab.utils


@epab.utils.run_once
def _safety():
    epab.utils.run('safety check --bare', mute=True)


@click.command()
def safety():
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    _safety()
