# coding=utf-8


import sys

import click

from epab.core import VERSION


def print_version(ctx: click.Context, _, value):
    if not value or ctx.resilient_parsing:
        return

    print(VERSION)
    sys.exit(0)
