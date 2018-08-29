# coding=utf-8

import datetime
from pathlib import Path

import elib_run
from mockito import and_, contains, mock, verify, verifyStubbedInvocationsAreUsed, when

import epab.exc
import epab.utils
from epab.cmd import _freeze as freeze
from epab.core import CTX, config


def test_freeze_cli(cli_runner):
    when(freeze)._freeze('version')
    cli_runner.invoke(freeze.freeze, ['version'])
    verifyStubbedInvocationsAreUsed()


def test_freeze():
    when(freeze)._install_pyinstaller()
    when(freeze)._patch('version')
    when(elib_run).run(...)
    when(epab.utils.AV).info(...)
    config.FREEZE_ENTRY_POINT.default = 'test'
    freeze._freeze('version')
    verifyStubbedInvocationsAreUsed()


def test_freeze_no_entry_point():
    when(freeze)._install_pyinstaller()
    when(freeze)._patch(...)
    when(elib_run).run(...)
    when(epab.utils.AV).info(...)
    when(epab.utils.AV).error(...)
    freeze._freeze('version')
    verify(freeze, times=0)._install_pyinstaller()
    verify(freeze, times=0)._patch()
    verify(elib_run, times=0).run(...)
    verify(epab.utils.AV, times=0).info(...)
    verify(epab.utils.AV).error(...)


def test_patch():
    repo = mock(spec=epab.utils.Repo)
    when(repo).get_current_branch().thenReturn('branch')
    when(repo).get_sha().thenReturn('sha')
    CTX.repo = repo
    now = datetime.datetime.utcnow()
    timestamp = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}'
    package_name = config.PACKAGE_NAME()
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
    when(epab.utils.AV).info('Patch OK')
    when(epab.utils).resource_path(...).thenReturn('dummy.exe')
    freeze._patch('version')
    verifyStubbedInvocationsAreUsed()


def test_install_pyinstaller_installed():
    when(epab.utils).info('checking PyInstaller installation')
    when(elib_run).run('pyinstaller --version').thenReturn(('version   ', 0))
    freeze._install_pyinstaller()
    verifyStubbedInvocationsAreUsed()


def test_install_pyinstaller_not_installed():
    when(epab.utils).info('checking PyInstaller installation')
    when(elib_run).run('pip install pyinstaller==3.3.1')
    when(epab.utils.AV).info('Installing PyInstaller')
    when(elib_run).run('pyinstaller --version') \
        .thenRaise(epab.exc.ExecutableNotFoundError) \
        .thenReturn(('version   ', 0))
    freeze._install_pyinstaller()
    verifyStubbedInvocationsAreUsed()


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
    when(freeze)._install_pyinstaller()
    when(freeze)._patch('version')
    when(elib_run).run(...)
    when(epab.utils.AV).info(...)
    config.FREEZE_ENTRY_POINT.default = 'test'
    config.PACKAGE_NAME.default = 'test'
    config.FREEZE_DATA_FILES.default = ['file1', 'file2']
    freeze._freeze('version')
    verifyStubbedInvocationsAreUsed()
    verify(elib_run).run(and_(contains('--add-data "file1"'), contains('--add-data "file2"')))
