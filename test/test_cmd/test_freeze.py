# coding=utf-8
import datetime

from epab.cmd import _freeze as freeze
from mockito import when, mock, verifyStubbedInvocationsAreUsed, verify, contains

import epab.utils
from epab.core import CONFIG


def test_freeze_cli(cli_runner):
    when(freeze)._freeze()
    cli_runner.invoke(freeze.freeze)
    verifyStubbedInvocationsAreUsed()


def test_freeze_flat_cli(cli_runner):
    when(freeze)._flat_freeze()
    cli_runner.invoke(freeze.flat_freeze)
    verifyStubbedInvocationsAreUsed()


def test_freeze():
    when(freeze)._install_pyinstaller()
    when(freeze)._patch()
    when(epab.utils).run(...)
    when(epab.utils.AV).info(...)
    CONFIG.entry_point = 'test'
    freeze._freeze()
    verifyStubbedInvocationsAreUsed()


def test_flat_freeze():
    when(freeze)._install_pyinstaller()
    when(epab.utils).run(...)
    CONFIG.entry_point = 'test'
    freeze._flat_freeze()
    verifyStubbedInvocationsAreUsed()


def test_freeze_no_entry_point():
    when(freeze)._install_pyinstaller()
    when(freeze)._patch()
    when(epab.utils).run(...)
    when(epab.utils.AV).info(...)
    when(epab.utils.AV).error(...)
    CONFIG.entry_point = ''
    freeze._freeze()
    verify(freeze, times=0)._install_pyinstaller()
    verify(freeze, times=0)._patch()
    verify(epab.utils, times=0).run(...)
    verify(epab.utils.AV, times=0).info(...)
    verify(epab.utils.AV).error(...)


def test_flat_freeze_no_entry_point():
    when(freeze)._install_pyinstaller()
    when(epab.utils).run(...)
    when(epab.utils.AV).info(...)
    when(epab.utils.AV).error(...)
    CONFIG.entry_point = ''
    freeze._flat_freeze()
    verify(freeze, times=0)._install_pyinstaller()
    verify(epab.utils, times=0).run(...)
    verify(epab.utils.AV, times=0).info(...)
    verify(epab.utils.AV).error(...)


def test_patch():
    when(epab.utils).get_git_version_info().thenReturn('0.0.1')
    raw_version = mock()
    raw_version.informational_version = 'informational_version'
    raw_version.commit_date = 'commit_date'
    when(epab.utils).get_raw_gitversion_info().thenReturn(raw_version)
    when(epab.utils).run(
        'dummy.exe '
        './dist/epab.exe '
        '/high 0.0.1 '
        '/va /pv 0.0.1 '
        '/s desc epab '
        '/s product epab '
        '/s title epab '
        '/s copyright 2018-132nd-etcher '
        '/s company 132nd-etcher '
        '/s SpecialBuild 0.0.1 '
        '/s PrivateBuild informational_version.commit_date '
        '/langid 1033'
    )
    when(epab.utils.AV).info('Patch OK')
    when(epab.utils).resource_path(...).thenReturn('dummy.exe')
    freeze._patch()
    verifyStubbedInvocationsAreUsed()


def test_install_pyinstaller():
    when(epab.utils).run('pip install pyinstaller==3.3.1')
    when(epab.utils).run(contains(' -m PyInstaller --version'), mute=True).thenReturn(('version   ', 0))
    when(epab.utils.AV).info('PyInstaller version: version')
    freeze._install_pyinstaller()
    verifyStubbedInvocationsAreUsed()


