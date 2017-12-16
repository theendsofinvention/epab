# coding=utf-8

import click

from epab.utils import write_reqs, repo_commit
from .changlog import chglog
from .release import release


@click.command()
@click.pass_context
def reqs(ctx: click.Context):
    """
    Write requirements files
    """
    write_reqs(ctx)
    repo_commit(ctx, 'chg: dev: update requirements [skip ci]')
