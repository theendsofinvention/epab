# coding=utf-8
"""
Pushes latest changes to origin
"""

import click

import epab.cmd
import epab.linters
import epab.utils
from epab.core import CTX


@epab.utils.stashed
def _push(ctx: click.Context):
    ctx.invoke(epab.linters.lint, amend=True)
    ctx.invoke(epab.cmd.pytest, long=True, exitfirst=True, failed_first=True)
    ctx.invoke(epab.cmd.reqs, amend=True)
    ctx.invoke(epab.cmd.chglog, amend=True)
    CTX.repo.push()


@click.command()
@click.pass_context
def push(ctx: click.Context):
    """
    Pushes latest changes to origin

    Args:
        ctx: click Context

    """
    _push(ctx)
