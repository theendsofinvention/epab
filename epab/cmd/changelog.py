# coding=utf-8
"""
Updates CHANGELOG.rst with the latest commits
"""

import re

import click
import epab.utils


@epab.utils.run_once
def _write_changelog(ctx, auto_commit):
    if ctx.obj['CONFIG'].get('disabled_changelog'):
        epab.utils.info('Skipping changelog update')
    else:
        epab.utils.ensure_exe('git')
        epab.utils.ensure_exe('gitchangelog')
        epab.utils.info('Writing changelog')
        changelog = epab.utils.do(ctx, ['gitchangelog'], mute_stdout=True)
        with open('CHANGELOG.rst', mode='w') as stream:
            stream.write(re.sub(r'(\s*\r\n){2,}', '\r\n', changelog))
        if auto_commit:
            files_to_add = ['CHANGELOG.rst']
            epab.utils.repo_commit(ctx, 'chg: dev: update changelog [auto]', files_to_add=files_to_add)


@click.command()
@click.pass_context
@click.option('-c', '--auto-commit', is_flag=True, help='Commit the changes')
def chglog(ctx, auto_commit):
    """
    Writes the changelog
    """
    _write_changelog(ctx, auto_commit)
