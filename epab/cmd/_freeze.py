# coding=utf-8
"""
Freeze package into exe
"""
import datetime
import functools
from pathlib import Path

import certifi
import click
import elib_run

import epab.cmd
import epab.exc
import epab.utils
from epab.core import CTX, config

VERPATCH_PATH = epab.utils.resource_path('epab', './vendor/verpatch.exe')
ICO = epab.utils.resource_path('epab', './vendor/app.ico')
BASE_CMD = [
    'pyinstaller',
    '--log-level=WARN',
    '--noconfirm',
    '--clean',
    '--icon', f'"{ICO}"',
    '--workpath', './build',
    '--distpath', './dist',
    '--add-data', f'"{certifi.where()};."',
    '--name'
]


def _install_pyinstaller():
    epab.utils.info('checking PyInstaller installation')
    _get_version = functools.partial(elib_run.run, 'pyinstaller --version')
    try:
        _get_version()
    except epab.exc.ExecutableNotFoundError:
        epab.utils.AV.info('Installing PyInstaller')
        elib_run.run('pip install pyinstaller==3.3.1')
        _get_version()


def _patch(version: str):
    now = datetime.datetime.utcnow()
    timestamp = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}'
    year = now.year
    cmd = [
        str(epab.utils.resource_path('epab', './vendor/verpatch.exe')),
        f'./dist/{config.PACKAGE_NAME()}.exe',
        '/high',
        version,
        '/va',
        '/pv', version,
        '/s', 'desc', config.PACKAGE_NAME(),
        '/s', 'product', config.PACKAGE_NAME(),
        '/s', 'title', config.PACKAGE_NAME(),
        '/s', 'copyright', f'{year}-etcher',
        '/s', 'company', 'etcher',
        '/s', 'SpecialBuild', version,
        '/s', 'PrivateBuild', f'{version}-'
                              f'{CTX.repo.get_current_branch()}_'
                              f'{CTX.repo.get_sha()}-{timestamp}',
        '/langid', '1033',
    ]
    elib_run.run(' '.join(cmd))
    epab.utils.AV.info('Patch OK')


def _freeze(version: str):
    if not config.FREEZE_ENTRY_POINT():
        epab.utils.AV.error('No entry point define, skipping freeze')
        return
    _install_pyinstaller()
    cmd = BASE_CMD + [config.PACKAGE_NAME(), '--onefile', config.FREEZE_ENTRY_POINT()]
    for data_file in config.FREEZE_DATA_FILES():
        cmd.append(f'--add-data "{data_file}"')
    elib_run.run(' '.join(cmd))
    elib_run.run('pipenv clean', failure_ok=True)
    epab.utils.AV.info('Freeze OK')
    _patch(version)


def _flat_freeze():
    if not config.FREEZE_ENTRY_POINT():
        epab.utils.AV.error('No entry point define, skipping freeze')
        return
    _install_pyinstaller()
    cmd = BASE_CMD + [config.PACKAGE_NAME(), config.FREEZE_ENTRY_POINT()]
    for data_file in config.FREEZE_DATA_FILES():
        cmd.append(f'--add-data "{data_file}"')
    elib_run.run(' '.join(cmd))


def _clean_spec():
    spec_file = Path(f'{config.PACKAGE_NAME()}.spec')
    spec_file.unlink()


@click.command()
@click.pass_context
@click.argument('version')
@click.option('-c', '--clean', is_flag=True, default=False, help='Clean spec file before freezing')
def freeze(ctx, version: str, clean: bool):
    """
    Freeze current package into a single file
    """
    if clean:
        _clean_spec()
    ctx.invoke(epab.cmd.compile_qt_resources)
    _freeze(version)


@click.command()
@click.pass_context
@click.option('-c', '--clean', is_flag=True, default=False, help='Clean spec file before freezing')
def flat_freeze(ctx, clean: bool):
    """
    Freeze current package into a directory
    """
    if clean:
        _clean_spec()
    ctx.invoke(epab.cmd.compile_qt_resources)
    _flat_freeze()
