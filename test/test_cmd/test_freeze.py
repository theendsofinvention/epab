# coding=utf-8

import datetime

from mockito import mock, verify, verifyStubbedInvocationsAreUsed, when

import epab.exc
import epab.utils
from epab.cmd import _freeze as freeze
from epab.core import CONFIG, CTX


def test_freeze_cli(cli_runner):
    when(freeze)._freeze('version')
    cli_runner.invoke(freeze.freeze, ['version'])
    verifyStubbedInvocationsAreUsed()


def test_freeze_flat_cli(cli_runner):
    when(freeze)._flat_freeze()
    cli_runner.invoke(freeze.flat_freeze)
    verifyStubbedInvocationsAreUsed()


def test_freeze():
    when(freeze)._install_pyinstaller()
    when(freeze)._patch('version')
    when(epab.utils).run(...)
    when(epab.utils.AV).info(...)
    CONFIG.entry_point = 'test'
    freeze._freeze('version')
    verifyStubbedInvocationsAreUsed()


def test_flat_freeze():
    when(freeze)._install_pyinstaller()
    when(epab.utils).run(...)
    CONFIG.entry_point = 'test'
    freeze._flat_freeze()
    verifyStubbedInvocationsAreUsed()


def test_freeze_no_entry_point():
    when(freeze)._install_pyinstaller()
    when(freeze)._patch(...)
    when(epab.utils).run(...)
    when(epab.utils.AV).info(...)
    when(epab.utils.AV).error(...)
    CONFIG.entry_point = ''
    freeze._freeze('version')
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
    repo = mock(spec=epab.utils.Repo)
    when(repo).get_current_branch().thenReturn('branch')
    when(repo).get_sha().thenReturn('sha')
    CTX.repo = repo
    now = datetime.datetime.utcnow()
    timestamp = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}'
    when(epab.utils).run(
        'dummy.exe '
        './dist/epab.exe '
        '/high version '
        '/va /pv version '
        '/s desc epab '
        '/s product epab '
        '/s title epab '
        f'/s copyright {now.year}-132nd-etcher '
        '/s company 132nd-etcher '
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
    when(epab.utils).run('pyinstaller --version').thenReturn(('version   ', 0))
    freeze._install_pyinstaller()
    verifyStubbedInvocationsAreUsed()


def test_install_pyinstaller_not_installed():
    when(epab.utils).info('checking PyInstaller installation')
    when(epab.utils).run('pip install pyinstaller==3.3.1')
    when(epab.utils.AV).info('Installing PyInstaller')
    when(epab.utils).run('pyinstaller --version') \
        .thenRaise(epab.exc.ExecutableNotFoundError) \
        .thenReturn(('version   ', 0))
    freeze._install_pyinstaller()
    verifyStubbedInvocationsAreUsed()
