# coding=utf-8
"""
Freeze package into exe
"""
import datetime
import functools
from pathlib import Path

import certifi
import click

import epab.cmd
import epab.exc
import epab.utils
from epab.core import CONFIG, CTX

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
    _get_version = functools.partial(epab.utils.run, 'pyinstaller --version')
    try:
        _get_version()
    except epab.exc.ExecutableNotFoundError:
        epab.utils.AV.info('Installing PyInstaller')
        epab.utils.run('pip install pyinstaller==3.3.1')
        _get_version()


def _patch(version: str):
    now = datetime.datetime.utcnow()
    timestamp = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}'
    year = now.year
    cmd = [
        str(epab.utils.resource_path('epab', './vendor/verpatch.exe')),
        f'./dist/{CONFIG.package}.exe',
        '/high',
        version,
        '/va',
        '/pv', version,
        '/s', 'desc', CONFIG.package,
        '/s', 'product', CONFIG.package,
        '/s', 'title', CONFIG.package,
        '/s', 'copyright', f'{year}-132nd-etcher',
        '/s', 'company', '132nd-etcher',
        '/s', 'SpecialBuild', version,
        '/s', 'PrivateBuild', f'{version}-'
                              f'{CTX.repo.get_current_branch()}_'
                              f'{CTX.repo.get_sha()}-{timestamp}',
        '/langid', '1033',
    ]
    epab.utils.run(' '.join(cmd))
    epab.utils.AV.info('Patch OK')


def _freeze(version: str):
    if not CONFIG.freeze__entry_point:
        epab.utils.AV.error('No entry point define, skipping freeze')
        return
    _install_pyinstaller()
    cmd = BASE_CMD + [CONFIG.package, '--onefile', CONFIG.freeze__entry_point]
    for data_file in CONFIG.freeze__data_files:
        cmd.append(f'--add-data "{data_file}"')
    epab.utils.add_to_gitignore('*.spec')
    epab.utils.run(' '.join(cmd))
    epab.utils.run('pipenv clean', failure_ok=True)
    epab.utils.AV.info('Freeze OK')
    _patch(version)


def _flat_freeze():
    if not CONFIG.freeze__entry_point:
        epab.utils.AV.error('No entry point define, skipping freeze')
        return
    _install_pyinstaller()
    cmd = BASE_CMD + [CONFIG.package, CONFIG.freeze__entry_point]
    for data_file in CONFIG.freeze__data_files:
        cmd.append(f'--add-data "{data_file}"')
    epab.utils.run(' '.join(cmd))


def _clean_spec():
    spec_file = Path(f'{CONFIG.package}.spec')
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
