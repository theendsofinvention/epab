# coding=utf-8
"""
Prints current version then exits
"""


import sys

import click

from epab.core import VERSION


def print_version(ctx: click.Context, _, value):
    """
    Prints current version then exits
    """
    if not value or ctx.resilient_parsing:
        return

    print(VERSION)
    sys.exit(0)
