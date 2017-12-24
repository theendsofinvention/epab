# coding=utf-8
"""
Updates CHANGELOG.rst with the latest commits
"""

import re

import click

from epab.utils import _info, do, ensure_exe, repo_commit, run_once


@run_once
def _write_changelog(ctx, auto_commit):
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
            files_to_add = ['CHANGELOG.rst']
            repo_commit(ctx, 'chg: dev: update changelog [auto]', files_to_add=files_to_add)


@click.command()
@click.pass_context
@click.option('-c', '--auto-commit', is_flag=True, help='Commit the changes')
def chglog(ctx, auto_commit):
    """
    Writes the changelog
    """
    _write_changelog(ctx, auto_commit)
