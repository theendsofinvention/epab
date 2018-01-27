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


def _release(ctx):
    if CTX.appveyor:
        epab.utils.info(f'Running on APPVEYOR')
        CTX.repo.checkout(os.getenv("APPVEYOR_REPO_BRANCH"))

    current_branch = CTX.repo.get_current_branch()
    next_version = epab.utils.get_git_version_info()
    epab.utils.info(f'Current version -> {VERSION}')
    epab.utils.info(f'Current branch  -> {current_branch}')
    epab.utils.info(f'Latest tag      -> {CTX.repo.get_latest_tag()}')
    epab.utils.info(f'Next version    -> {next_version}')

    if CTX.appveyor:
        epab.utils.run(f'appveyor UpdateBuild -Version '
                       f'{next_version}-'
                       f'{os.getenv("APPVEYOR_BUILD_NUMBER")}-'
                       f'{os.getenv("APPVEYOR_REPO_COMMIT")}')

    epab.utils.info('Checking repo')
    if CTX.repo.is_dirty(untracked=True):
        epab.utils.error('Repository is dirty, cannot release')
        exit(1)

    if CTX.dry_run:
        epab.utils.info('Skipping release; DRY RUN')
        return

    CTX.stash = False
    epab.utils.info(f'Running on commit: {CTX.repo.latest_commit()}')
    ctx.invoke(epab.linters.lint)
    if CTX.repo.is_dirty(untracked=True):  # pragma: no cover
        for changed_file in CTX.repo.changed_files():
            print(CTX.repo.repo.git.diff(changed_file))
        epab.utils.error('Linters produced artifacts, aborting release')
        exit(1)

    ctx.invoke(epab.cmd.pytest, long=True)
    if CTX.appveyor:
        epab.utils.info('Uploading coverage info')
        epab.utils.run('pip install --upgrade codacy-coverage')
        epab.utils.run('python-codacy-coverage -r coverage.xml')
        _copy_artifacts()

    ctx.invoke(epab.cmd.reqs, stage=True)

    ctx.invoke(epab.cmd.chglog, stage=True, next_version=next_version)

    CTX.repo.commit(f'release {next_version}', allow_empty=True)
    CTX.repo.tag(next_version)

    _clean()

    python_exe = sys.executable.replace('\\', '/')
    epab.utils.run(f'{python_exe} setup.py sdist bdist_wheel')
    epab.utils.run(f'twine upload dist/* --skip-existing', mute=True)

    CTX.repo.push()


@click.command()
@click.pass_context
def release(ctx):
    """
    This is meant to be used as a Git pre-push hook
    """
    _release(ctx)
