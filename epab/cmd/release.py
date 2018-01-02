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
import epab.utils

from .changelog import chglog
from .test_runner import pytest


def _clean(ctx):
    """
    Cleans up build dir
    """
    epab.utils._info(f'Cleaning project directory...')
    if epab.utils.dry_run(ctx):
        return
    folders_to_cleanup = [
        '.eggs',
        'build',
        f'{ctx.obj["CONFIG"]["package"]}.egg-info',
    ]
    for folder in folders_to_cleanup:
        if os.path.exists(folder):
            epab.utils._info(f'\tremoving: {folder}')
            shutil.rmtree(folder)


@click.command()
@click.argument('new_version', required=False)
@click.pass_context
def release(ctx, new_version):
    """
    This is meant to be used as a Git pre-push hook
    """
    current_branch = epab.utils.repo_get_current_branch(ctx)
    if 'develop' not in [current_branch, os.getenv('APPVEYOR_REPO_BRANCH')]:
        epab.utils._error(
            f'Not on develop; skipping release (current branch: {current_branch})')
        exit(0)

    if current_branch == 'HEAD' and os.getenv('APPVEYOR_REPO_BRANCH') == 'develop':
        epab.utils.repo_checkout(ctx, 'develop')

    epab.utils._info('Making new release')

    ctx.invoke(pytest)

    ctx.invoke(lint, auto_commit=True)

    ctx.invoke(reqs, auto_commit=True)

    on_tag = epab.utils.repo_is_on_tag(ctx)

    if on_tag:
        new_version = epab.utils.repo_get_latest_tag(ctx)
        epab.utils._info(f'Using existing tag as version: {new_version}')
        ctx.invoke(chglog, auto_commit=True)
    else:
        new_version = epab.utils.bump_version(ctx, new_version)
        epab.utils._info(f'New version: {new_version}')
        epab.utils.repo_tag(ctx, new_version)
        ctx.invoke(chglog, auto_commit=True)
        epab.utils.repo_remove_tag(ctx, new_version)

    epab.utils.repo_checkout(ctx, 'master')
    epab.utils.repo_merge(ctx, 'develop')

    if not on_tag:
        epab.utils.repo_tag(ctx, new_version)

    try:

        _clean(ctx)

        if epab.utils.dry_run(ctx):
            epab.utils._info('DRYRUN: All good!')
            return
        epab.utils.do(ctx, sys.executable.replace('\\', '/') + ' setup.py bdist_wheel')
        epab.utils.do(ctx, 'twine upload dist/* --skip-existing',
                      mute_stdout=True, mute_stderr=True)

        epab.utils.repo_checkout(ctx, 'develop')
        epab.utils.repo_push(ctx)

        if ctx.obj["CONFIG"]["package"] != 'epab':
            epab.utils.do(ctx, 'pip install -e .')
        epab.utils._info('All good!')

    except SystemExit:
        epab.utils.repo_checkout(ctx, 'develop')
        _clean(ctx)
        epab.utils.repo_remove_tag(ctx, new_version)

        if ctx.obj["CONFIG"]["package"] != 'epab':
            epab.utils.do(ctx, 'pip install -e .')
        raise
