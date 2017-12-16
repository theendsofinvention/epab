# coding=utf-8

import click

from epab.utils import write_reqs, repo_commit
from .changlog import chglog
from .release import release


@click.command()
@click.option('-c', '--auto-commit', is_flag=True, help='Commit the changes')
@click.pass_context
def reqs(ctx: click.Context, auto_commit: bool):
    """
    Write requirements files
    """
    write_reqs(ctx, auto_commit)
