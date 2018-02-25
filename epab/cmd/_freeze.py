# coding=utf-8
"""
Freeze package into exe
"""
import datetime
import sys

import certifi
import click

import epab.utils
from epab.core import CONFIG

GIT_VERSION_PATH = epab.utils.resource_path('epab', './vendor/GitVersion_4.0.0-beta0013/gitversion.exe')
VERPATCH_PATH = epab.utils.resource_path('epab', './vendor/verpatch.exe')
ICO = epab.utils.resource_path('epab', './vendor/app.ico')


def _install_pyinstaller():
    epab.utils.run('pip install --upgrade pyinstaller')
    pyinstaller_version, _ = epab.utils.run(f'{sys.executable} -m PyInstaller --version')
    pyinstaller_version = pyinstaller_version.strip()
    epab.utils.AV.info(f'PyInstaller version: {pyinstaller_version}')


def _patch():
    version = epab.utils.get_git_version_info()
    git_version_info = epab.utils.get_raw_gitversion_info()
    year = datetime.datetime.now().year
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
        '/s', 'PrivateBuild', f'{git_version_info.informational_version}.{git_version_info.commit_date}',
        '/langid', '1033',
    ]
    epab.utils.run(' '.join(cmd))
    epab.utils.AV.info('Patch OK')


def _freeze():
    if not CONFIG.entry_point:
        epab.utils.error('No entry point define, skipping freeze')
        return
    _install_pyinstaller()
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--log-level=WARN',
        '--noconfirm', '--onefile', '--clean',
        '--icon', f'"{ICO}"',
        '--workpath', './build',
        '--distpath', './dist',
        '--add-data', f'"{certifi.where()};."',
        '--name', CONFIG.package,
        CONFIG.entry_point,
    ]
    for data_file in CONFIG.data_files:
        cmd.append(f'--add-data "{data_file}"')
    epab.utils.run(' '.join(cmd))
    epab.utils.AV.info('Freeze OK')
    _patch()


@click.command()
def freeze():
    """
    Freeze current package
    """
    _freeze()
