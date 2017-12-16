# coding=utf-8
"""
Click command to write the requirements
"""

import click

from epab.utils import write_reqs


@click.command()
@click.option('-c', '--auto-commit', is_flag=True, help='Commit the changes')
@click.pass_context
def reqs(ctx: click.Context, auto_commit: bool):
    """
    Write requirements files
    """
    write_reqs(ctx, auto_commit)
