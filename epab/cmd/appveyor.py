# coding=utf-8

import os

import click

from epab import __version__
from epab.utils import _info, do, repo_get_latest_tag
from .release import release


def _appveyor_branch():
    return os.getenv('APPVEYOR_REPO_BRANCH')


def _appveyor_commit():
    return os.getenv('APPVEYOR_REPO_COMMIT')


def _appveyor_build():
    return os.getenv('APPVEYOR_BUILD_NUMBER')


def _appveyor_update_build(ctx: click.Context, version: str):
    do(ctx, ['appveyor', 'UpdateBuild', '-Version', f'{version}-{_appveyor_build()}-{_appveyor_commit()}'])


@click.command()
@click.pass_context
def appveyor(ctx: click.Context):
    _info('RUNNING APPVEYOR RELEASE')
    _info(f'Current version: {__version__}')
    _info(f'Latest tag: {repo_get_latest_tag(ctx)}')
    _appveyor_update_build(ctx, repo_get_latest_tag(ctx))

    _info('Installing GitChangelog')
    do(ctx, ['pip', 'install', '--upgrade', 'gitchangelog'])

    _info('Installing current package dependencies')
    do(ctx, ['pipenv', 'install', '-d', '.'])

    _info('Running tests')
    do(ctx, ['pipenv', 'install', '-d', '.'])

    _info('Uploading coverage info')
    do(ctx, ['pip', 'install', '--upgrade', 'codacy-coverage'])
    do(ctx, ['python-codacy-coverage', '-r', 'coverage.xml'])

    _info('Installing current package in editable mode')
    do(ctx, ['pip', 'install', '-e', '.'])

    if os.path.exists('appveyor.yml'):
        _info('Removing leftover "appveyor.yml" file')
        os.unlink('appveyor.yml')

    if os.getenv('APPVEYOR_REPO_BRANCH') == 'develop':
        _info('We\'re on develop; making new release')
        ctx.invoke(release)
    else:
        _info('Not on develop, skipping release')

    _appveyor_update_build(ctx, repo_get_latest_tag(ctx))
    _info('ALL DONE')
