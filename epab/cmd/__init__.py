# coding=utf-8

import click

from epab.utils import write_reqs
from .changlog import chglog
from .release import release


@click.command()
@click.pass_context
def reqs(ctx: click.Context):
    """
    Write requirements files
    """
    write_reqs(ctx)
