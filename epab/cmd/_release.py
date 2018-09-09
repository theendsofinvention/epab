# coding=utf-8
"""
Creates a wheel from a Github repo
"""
import logging
import os
import shutil
import sys
from pathlib import Path

import click
import elib_run

import epab.cmd
import epab.linters
import epab.utils
from epab import __version__
from epab.core import CTX, config

LOGGER = logging.getLogger('EPAB')


def _clean():
    """
    Cleans up build dir
    """
    LOGGER.info('Cleaning project directory...')
    folders_to_cleanup = [
        '.eggs',
        'build',
        f'{config.PACKAGE_NAME()}.egg-info',
    ]
    for folder in folders_to_cleanup:
        if os.path.exists(folder):
            LOGGER.info('\tremoving: %s', folder)
            shutil.rmtree(folder)


def _copy_artifacts():
    if config.ARTIFACTS():
        folder = Path('./artifacts')
        folder.mkdir(exist_ok=True)
        for pattern in config.ARTIFACTS():
            for artifact in Path('.').glob(pattern):
                src = str(artifact.absolute())
                dst = str(folder.absolute())
                shutil.copy(src, dst)
                LOGGER.info('copying artifact: %s', f'{src} -> {dst}')


def _check_dirty(reason: str):
    LOGGER.info('checking repo')
    if CTX.repo.is_dirty(untracked=True):
        LOGGER.error('repository is dirty: %s', reason)
        sys.exit(1)


def _remove_av_artifacts():
    if CTX.appveyor:
        LOGGER.info(f'running on APPVEYOR')
        if Path('appveyor.yml').exists():
            Path('appveyor.yml').unlink()
        CTX.repo.checkout(os.getenv('APPVEYOR_REPO_BRANCH'))


def _print_build_info(current_branch: str, next_version: str):
    info = [
        f'Current EPAB version -> {__version__}',
        f'Current branch  -> {current_branch}',
        f'Latest tag      -> {CTX.repo.get_latest_tag()}',
        f'Next version    -> {next_version}',
    ]
    LOGGER.info('build info: %s', ','.join(info))


def _run_linters(ctx):
    ctx.invoke(epab.linters.lint)
    _check_dirty('linters produced artifacts')
    LOGGER.info('linters OK')


def _run_tests(ctx):
    ctx.invoke(epab.cmd.pytest, long=True)
    LOGGER.info('tests OK')


def _create_wheel():
    python_exe = sys.executable.replace('\\', '/')
    elib_run.run(f'{python_exe} setup.py bdist_wheel')
    LOGGER.info('setup OK')


def _upload_to_twine():
    elib_run.run(f'twine upload dist/* --skip-existing', mute=True)
    LOGGER.info('twine OK')


def _update_av_build_name(next_version):
    build_version = f'{next_version}-{os.getenv("APPVEYOR_BUILD_NUMBER")}-{os.getenv("APPVEYOR_REPO_COMMIT")}'
    elib_run.run(f'appveyor UpdateBuild -Version {build_version}')
    LOGGER.info('build version: %s', build_version)


def _release(ctx: click.Context):
    CTX.stash = False

    _remove_av_artifacts()

    current_branch = CTX.repo.get_current_branch()
    next_version = epab.utils.get_next_version()

    _print_build_info(current_branch, next_version)

    _check_dirty('initial check failed')

    LOGGER.info('running on commit: %s', CTX.repo.latest_commit())

    _run_linters(ctx)

    _run_tests(ctx)

    if CTX.appveyor:
        _copy_artifacts()

    CTX.repo.tag(next_version, overwrite=True)

    _clean()

    _check_dirty('last check before build')

    ctx.invoke(epab.cmd.graph)

    _create_wheel()

    if current_branch == 'master':
        _upload_to_twine()

    if current_branch != 'master':
        CTX.repo.push_tags()

    if CTX.appveyor:
        epab.utils.AV.set_env_var('EPAB_VERSION', next_version)
        _update_av_build_name(next_version)


@click.command()
@click.pass_context
def release(ctx):
    """
    Runs tests and creates:

    - wheel binary distribution and pushes it to the cheese shop
    - release tag and pushes it back to origin
    """
    _release(ctx)
