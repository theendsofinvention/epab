# coding=utf-8
"""
Creates a wheel from a Github repo
"""
import os
import shutil
import sys
from pathlib import Path

import click

import epab.cmd
import epab.linters
import epab.utils
from epab.core import CONFIG, CTX, VERSION


def _clean():
    """
    Cleans up build dir
    """
    epab.utils.info(f'Cleaning project directory...')
    if CTX.dry_run:
        return
    folders_to_cleanup = [
        '.eggs',
        'build',
        f'{CONFIG.package}.egg-info',
    ]
    for folder in folders_to_cleanup:
        if os.path.exists(folder):
            epab.utils.info(f'\tremoving: {folder}')
            shutil.rmtree(folder)


def _copy_artifacts():
    if CONFIG.artifacts:
        epab.utils.info('Copying artifacts')
        folder = Path('./artifacts')
        folder.mkdir(exist_ok=True)
        assert isinstance(CONFIG.artifacts, list)
        for pattern in CONFIG.artifacts:
            for artifact in Path('.').glob(pattern):
                src = str(artifact.absolute())
                dst = str(folder.absolute())
                epab.utils.info(f'Copying: {src} -> {dst}')
                shutil.copy(src, dst)


def _check_dirty(reason: str):
    epab.utils.info('Checking repo')
    print(CTX.repo.status())
    if CTX.repo.is_dirty(untracked=True):
        epab.utils.error(f'Aborting release: {reason}')
        sys.exit(1)


def _remove_av_artifacts():
    if CTX.appveyor:
        epab.utils.info(f'Running on APPVEYOR')
        if Path('appveyor.yml').exists():
            Path('appveyor.yml').unlink()
        CTX.repo.checkout(os.getenv('APPVEYOR_REPO_BRANCH'))


def _print_build_info(current_branch: str, next_version: str):
    epab.utils.info(f'Current version -> {VERSION}')
    epab.utils.info(f'Current branch  -> {current_branch}')
    epab.utils.info(f'Latest tag      -> {CTX.repo.get_latest_tag()}')
    epab.utils.info(f'Next version    -> {next_version}')


def _run_linters(ctx):
    ctx.invoke(epab.linters.lint)

    _check_dirty('linters produced artifacts')


def _install_codacy_coverage():
    epab.utils.info('Uploading coverage info')
    epab.utils.run('pip install --upgrade codacy-coverage')
    epab.utils.run('python-codacy-coverage -r coverage.xml')


def _run_tests(ctx):
    ctx.invoke(epab.cmd.pytest, long=True)


def _upload_to_twine():
    epab.utils.run(f'twine upload dist/* --skip-existing', mute=True)


def _update_av_build_name(next_version):
    epab.utils.run(f'appveyor UpdateBuild -Version '
                   f'{next_version}-'
                   f'{os.getenv("APPVEYOR_BUILD_NUMBER")}-'
                   f'{os.getenv("APPVEYOR_REPO_COMMIT")}')


def _release(ctx: click.Context):
    CTX.stash = False

    _remove_av_artifacts()

    current_branch = CTX.repo.get_current_branch()
    next_version = epab.utils.get_git_version_info()

    _print_build_info(current_branch, next_version)

    epab.utils.info('Checking repo')
    _check_dirty('repository is dirty')

    if CTX.dry_run:
        epab.utils.info('Skipping release; DRY RUN')
        return

    epab.utils.info(f'Running on commit: {CTX.repo.latest_commit()}')

    _run_linters(ctx)

    _run_tests(ctx)

    if CTX.appveyor:
        _install_codacy_coverage()
        _copy_artifacts()

    CTX.repo.tag(next_version, overwrite=True)

    _clean()

    python_exe = sys.executable.replace('\\', '/')
    _check_dirty('last check before building')
    epab.utils.run(f'{python_exe} setup.py sdist bdist_wheel')

    if current_branch == 'master':
        _upload_to_twine()

    if current_branch != 'master':
        CTX.repo.push_tags()

    os.putenv('EPAB_VERSION', next_version)

    if CTX.appveyor:
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
