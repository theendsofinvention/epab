# coding=utf-8
"""
Creates a wheel from a Github repo
"""
import os
import shutil
import sys

import click

from epab.cmd.requirements import reqs
from epab.linters import lint
from epab.utils import (_error, _info, bump_version, do, dry_run, repo_checkout, repo_get_current_branch, repo_merge,
                        repo_push, repo_remove_tag, repo_tag)

from .changelog import chglog
from .test_runner import pytest


def _clean(ctx):
    """
    Cleans up build dir
    """
    _info(f'Cleaning project directory...')
    if dry_run(ctx):
        return
    folders_to_cleanup = [
        '.eggs',
        'build',
        f'{ctx.obj["CONFIG"]["package"]}.egg-info',
    ]
    for folder in folders_to_cleanup:
        if os.path.exists(folder):
            _info(f'\tremoving: {folder}')
            shutil.rmtree(folder)


@click.command()
@click.argument('new_version', required=False)
@click.pass_context
def release(ctx, new_version):
    """
    This is meant to be used as a Git pre-push hook
    """
    current_branch = repo_get_current_branch(ctx)
    if 'develop' not in [current_branch, os.getenv('APPVEYOR_REPO_BRANCH')]:
        _error(
            f'Not on develop; skipping release (current branch: {current_branch})')
        exit(0)

    if current_branch == 'HEAD' and os.getenv('APPVEYOR_REPO_BRANCH') == 'develop':
        repo_checkout(ctx, 'develop')

    _info('Making new release')

    ctx.invoke(pytest)

    ctx.invoke(lint, auto_commit=True)

    ctx.invoke(reqs, auto_commit=True)

    new_version = bump_version(ctx, new_version)
    _info(f'New version: {new_version}')
    repo_tag(ctx, new_version)
    ctx.invoke(chglog, auto_commit=True)
    repo_remove_tag(ctx, new_version)

    repo_checkout(ctx, 'master')
    repo_merge(ctx, 'develop')
    repo_tag(ctx, new_version)

    try:

        _clean(ctx)

        if dry_run(ctx):
            _info('DRYRUN: All good!')
            return
        do(ctx, sys.executable.replace('\\', '/') + ' setup.py bdist_wheel')
        do(ctx, 'twine upload dist/* --skip-existing',
           mute_stdout=True, mute_stderr=True)

        repo_checkout(ctx, 'develop')
        repo_push(ctx)

        if ctx.obj["CONFIG"]["package"] != 'epab':
            do(ctx, 'pip install -e .')
        _info('All good!')

    except SystemExit:
        repo_checkout(ctx, 'develop')
        _clean(ctx)
        repo_remove_tag(ctx, new_version)

        if ctx.obj["CONFIG"]["package"] != 'epab':
            do(ctx, 'pip install -e .')
        raise
