# coding=utf-8
"""
Manages the release process on Appveyor
"""

import os

import click
import epab.linters
import epab.utils
from epab import __version__

from .release import release
from .test_runner import pytest


def _appveyor_branch():
    return os.getenv('APPVEYOR_REPO_BRANCH')


def _appveyor_commit():
    return os.getenv('APPVEYOR_REPO_COMMIT')


def _appveyor_build():
    return os.getenv('APPVEYOR_BUILD_NUMBER')


def _appveyor_update_build(ctx: click.Context, version: str):
    epab.utils.do(ctx, ['appveyor', 'UpdateBuild', '-Version', f'{version}-{_appveyor_build()}-{_appveyor_commit()}'])


@epab.utils.run_once
def _appveyor(ctx):
    epab.utils.info('RUNNING APPVEYOR RELEASE')
    epab.utils.info(f'Current version: {__version__}')
    epab.utils.info(f'Latest tag: {epab.utils.repo_get_latest_tag(ctx)}')
    _appveyor_update_build(ctx, epab.utils.repo_get_latest_tag(ctx))

    epab.utils.info('Running tests')
    ctx.invoke(pytest)

    epab.utils.info('Uploading coverage info')
    epab.utils.do(ctx, ['pip', 'install', '--upgrade', 'codacy-coverage'])
    epab.utils.do(ctx, ['python-codacy-coverage', '-r', 'coverage.xml'])

    # Covered by AV
    # if not ctx.obj['CONFIG']['package'] == 'epab':
    #     info('Installing current package with pipenv')
    #     do(ctx, ['pipenv', 'install', '.'])

    if os.path.exists('appveyor.yml'):
        epab.utils.info('Removing leftover "appveyor.yml" file')
        os.unlink('appveyor.yml')

    commit_msg = os.getenv('APPVEYOR_REPO_COMMIT_MESSAGE_EXTENDED')
    if commit_msg:
        if 'release ' in commit_msg.lower():
            tag = commit_msg.lower().replace('release ', '')
            epab.utils.info(f'using tag from commit message: {tag}')
            ctx.obj['new_version'] = tag

    if os.getenv('APPVEYOR_REPO_BRANCH') == 'develop':
        epab.utils.info('We\'re on develop; making new release')
        ctx.invoke(release)
    else:
        epab.utils.info('Not on develop, skipping release')
        ctx.invoke(epab.linters.lint, auto_commit=False)

    _appveyor_update_build(ctx, epab.utils.repo_get_latest_tag(ctx))
    epab.utils.info('ALL DONE')


@click.command()
@click.pass_context
def appveyor(ctx: click.Context):
    """
    Manages the release process on Appveyor
    """
    _appveyor(ctx)
