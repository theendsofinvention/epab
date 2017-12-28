# coding=utf-8
"""
Safety linter
"""

import click

from epab.utils import do, run_once


@run_once
def _safety(ctx):
    do(ctx, ['safety', 'check', '--bare'])


@click.command()
@click.pass_context
def safety(ctx):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    _safety(ctx)
