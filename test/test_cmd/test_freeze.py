# coding=utf-8

import datetime
from pathlib import Path

import elib_run
import pytest
from mockito import and_, contains, expect, mock, when

import epab.exc
import epab.utils
from epab.cmd import _freeze as freeze
from epab.cmd._freeze import _format_data_file, site_package
from epab.core import CTX, config


def test_freeze_cli(cli_runner):
    when(freeze)._freeze('version')
    cli_runner.invoke(freeze.freeze, ['version'])


def test_freeze():
    config.FREEZE_ENTRY_POINT.default = 'test'

    when(freeze)._install_pyinstaller()
    when(freeze)._patch('version')

    expect(elib_run).run('pipenv clean', failure_ok=True)
    expect(elib_run).run(contains('pyinstaller --log-level=WARN'), timeout=300)

    freeze._freeze('version')


def test_freeze_no_entry_point(caplog):
    expect(freeze, times=0)._install_pyinstaller()
    expect(freeze, times=0)._patch(...)

    freeze._freeze('version')

    assert 'no entry point defined, skipping freeze' in caplog.text


def test_patch():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    now = datetime.datetime.utcnow()
    timestamp = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}'
    package_name = config.PACKAGE_NAME()

    when(repo).get_current_branch().thenReturn('branch')
    when(repo).get_sha().thenReturn('sha')
    when(elib_run).run(
        'dummy.exe '
        f'./dist/{package_name}.exe '
        '/high version '
        '/va /pv version '
        f'/s desc {package_name} '
        f'/s product {package_name} '
        f'/s title {package_name} '
        f'/s copyright {now.year}-etcher '
        '/s company etcher '
        '/s SpecialBuild version '
        f'/s PrivateBuild version-branch_sha-{timestamp} '
        '/langid 1033'
    )
    when(epab.utils).resource_path(...).thenReturn('dummy.exe')

    freeze._patch('version')


def test_install_pyinstaller_installed():
    expect(elib_run).run('pyinstaller --version').thenReturn(('version   ', 0))
    freeze._install_pyinstaller()


def test_install_pyinstaller_not_installed():
    when(elib_run).run('pip install pyinstaller==3.4')
    when(elib_run).run('pyinstaller --version') \
        .thenRaise(elib_run.ExecutableNotFoundError('pyinstaller')) \
        .thenReturn(('version', 0))

    freeze._install_pyinstaller()


def test_clean_spec(cli_runner):
    config.PACKAGE_NAME.default = 'test'
    config.FREEZE_ENTRY_POINT.default = 'test'
    spec_file = Path('test.spec')
    spec_file.touch()
    version = '0.1.0'

    when(freeze)._freeze(version)

    cli_runner.invoke(freeze.freeze, [version, '-c'])

    assert not spec_file.exists()


def test_with_data_files():
    config.FREEZE_ENTRY_POINT.default = 'test'
    config.PACKAGE_NAME.default = 'test'
    config.FREEZE_DATA_FILES.default = ['file1', 'file2']

    when(freeze)._install_pyinstaller()
    when(freeze)._patch('version')
    expect(elib_run).run('pipenv clean', failure_ok=True)
    expect(elib_run).run(and_(
        contains('pyinstaller --log-level=WARN'),
        contains('--add-data "file1"'),
        contains('--add-data "file2"')), timeout=300)

    freeze._freeze('version')


@pytest.mark.parametrize(
    'data_file_src, expected',
    [
        ('{site_package}/pytest.py', site_package() + '/pytest.py')
    ]

)
def test_format_data_file(data_file_src, expected):
    actual = _format_data_file(data_file_src)
    assert expected == actual
    assert Path(actual).exists()
