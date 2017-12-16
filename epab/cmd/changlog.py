# coding=utf-8


import re

import click
from epab.utils import _info, do, ensure_exe, repo_commit


@click.command()
@click.pass_context
@click.option('-c', '--auto-commit', is_flag=True, help='Commit the changes')
def chglog(ctx, auto_commit):
    """
    Writes the changelog

    Returns:
        bool: returns true if changes have been committed to the repository
    """
    if ctx.obj['CONFIG'].get('disabled_changelog'):
        _info('Skipping changelog update')
    else:
        ensure_exe('git')
        ensure_exe('gitchangelog')
        _info('Writing changelog')
        changelog = do(ctx, ['gitchangelog'], mute_stdout=True)
        with open('CHANGELOG.rst', mode='w') as stream:
            stream.write(re.sub(r'(\s*\r\n){2,}', '\r\n', changelog))
        if auto_commit:
            repo_commit(ctx, 'chg: dev: update changelog [auto] [skip ci]')
