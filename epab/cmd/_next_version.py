# coding=utf-8


import sys

import click

import epab.utils
from epab.core import CONFIG


def next_version(ctx: click.Context, _, value):
    CONFIG.quiet = True

    if not value or ctx.resilient_parsing:
        return

    print(epab.utils.get_git_version_info())
    sys.exit(0)
