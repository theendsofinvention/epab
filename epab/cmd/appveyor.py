# coding=utf-8
"""
Manages the release process on Appveyor
"""

import os

import click

from epab import __version__
from epab.linters import lint
from epab.utils import info, do, repo_get_latest_tag, run_once

from .release import release
from .test_runner import pytest


def _appveyor_branch():
    return os.getenv('APPVEYOR_REPO_BRANCH')


def _appveyor_commit():
    return os.getenv('APPVEYOR_REPO_COMMIT')


def _appveyor_build():
    return os.getenv('APPVEYOR_BUILD_NUMBER')


def _appveyor_update_build(ctx: click.Context, version: str):
    do(ctx, ['appveyor', 'UpdateBuild', '-Version',
             f'{version}-{_appveyor_build()}-{_appveyor_commit()}'])


@run_once
def _appveyor(ctx):
    info('RUNNING APPVEYOR RELEASE')
    info(f'Current version: {__version__}')
    info(f'Latest tag: {repo_get_latest_tag(ctx)}')
    _appveyor_update_build(ctx, repo_get_latest_tag(ctx))

    info('Installing GitChangelog')
    do(ctx, ['pip', 'install', '--upgrade', 'gitchangelog'])

    info('Running tests')
    ctx.invoke(pytest)

    info('Uploading coverage info')
    do(ctx, ['pip', 'install', '--upgrade', 'codacy-coverage'])
    do(ctx, ['python-codacy-coverage', '-r', 'coverage.xml'])

    # Covered by AV
    # if not ctx.obj['CONFIG']['package'] == 'epab':
    #     info('Installing current package with pipenv')
    #     do(ctx, ['pipenv', 'install', '.'])

    if os.path.exists('appveyor.yml'):
        info('Removing leftover "appveyor.yml" file')
        os.unlink('appveyor.yml')

    if os.getenv('APPVEYOR_REPO_BRANCH') == 'develop':
        info('We\'re on develop; making new release')
        ctx.invoke(release)
    else:
        info('Not on develop, skipping release')
        ctx.invoke(lint, auto_commit=False)

    _appveyor_update_build(ctx, repo_get_latest_tag(ctx))
    info('ALL DONE')


@click.command()
@click.pass_context
def appveyor(ctx: click.Context):
    """
    Manages the release process on Appveyor
    """
    _appveyor(ctx)
