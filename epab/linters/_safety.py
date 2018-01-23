# coding=utf-8
"""
Safety linter
"""

import click
import epab.utils


@epab.utils.run_once
def _safety(ctx):
    epab.utils.do(ctx, ['safety', 'check', '--bare'])


@click.command()
@click.pass_context
def safety(ctx):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    _safety(ctx)
