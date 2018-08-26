# coding=utf-8
"""
Prints next version (according to Gitversion run) then exits
"""

import sys

import click

import epab.utils
from epab.core import CTX, config


def next_version(ctx: click.Context, _, value):
    """
    Prints next version (according to Gitversion run) then exits
    """

    if not value or ctx.resilient_parsing:
        return

    config.QUIET.default = True

    CTX.repo = epab.utils.Repo()

    print(epab.utils.get_next_version())
    sys.exit(0)
