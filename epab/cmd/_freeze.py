# coding=utf-8
"""
Freeze package into exe
"""
import datetime
import functools
import logging
from distutils.sysconfig import get_python_lib as site_package  # pylint: disable=import-error
from pathlib import Path

import certifi
import click
import elib_run

import epab.cmd
import epab.exc
import epab.utils
from epab.core import CTX, config

LOGGER = logging.getLogger('EPAB')
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


def _get_site_package_directory() -> str:
    return site_package()


_DATA_FILE_REPLACE = {
    '{site_package}': _get_site_package_directory(),
}


def _format_data_file(data_file: str) -> str:
    for _replacement_src, _replacement_tgt in _DATA_FILE_REPLACE.items():
        data_file = data_file.replace(_replacement_src, _replacement_tgt)
    LOGGER.debug('formatted data file str: %s', data_file)
    return data_file


def _install_pyinstaller():
    LOGGER.info('checking PyInstaller installation')
    _get_version = functools.partial(elib_run.run, 'pyinstaller --version')
    try:
        _get_version()
    except elib_run.ExecutableNotFoundError:
        LOGGER.info('installing PyInstaller')
        elib_run.run('pip install pyinstaller==3.4')
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
    LOGGER.info('patch OK')


def _freeze(version: str):
    if not config.FREEZE_ENTRY_POINT():
        LOGGER.error('no entry point defined, skipping freeze')
        return
    _install_pyinstaller()
    cmd = BASE_CMD + [config.PACKAGE_NAME(), '--noupx --onefile', config.FREEZE_ENTRY_POINT()]
    for data_file in config.FREEZE_DATA_FILES():
        LOGGER.debug('appending data file: %s', data_file)
        data_file = _format_data_file(data_file)
        cmd.append(f'--add-data "{data_file}"')
    LOGGER.info('freezing %s', config.PACKAGE_NAME)
    elib_run.run(' '.join(cmd), timeout=300)
    elib_run.run('pipenv clean', failure_ok=True)
    LOGGER.info('freeze OK')
    _patch(version)


def _clean_spec():
    spec_file = Path(f'{config.PACKAGE_NAME()}.spec')
    spec_file.unlink()


@click.command()
@click.pass_context
@click.argument('version')
@click.option('-c', '--clean', is_flag=True, default=False, help='Clean spec file before freezing')
@click.option('-v', '--version', default=None, help='Specify the version number for freezing')
def freeze(ctx, version: str, clean: bool):
    """
    Freeze current package into a single file
    """
    if clean:
        _clean_spec()
    ctx.invoke(epab.cmd.compile_qt_resources)
    _freeze(version)
