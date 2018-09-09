# coding=utf-8
import shutil
import subprocess
from pathlib import Path

import elib_run
import pytest
# noinspection PyProtectedMember
from mockito import (ANY, and_, contains, expect, mock, verify, when)

import epab.linters
import epab.utils
# noinspection PyProtectedMember
from epab.cmd import _release
from epab.core import CTX, config

RELEASE_ARTIFACTS = ['.eggs', 'build', 'package.egg-info']


def _create_dummy_release_artifacts():
    Path('.eggs').mkdir()
    Path('build').mkdir()
    Path('package.egg-info').mkdir()


def test_release():
    ctx = mock()
    repo = mock()
    CTX.repo = repo

    when(CTX.repo).is_dirty(untracked=True).thenReturn(False)

    expect(elib_run).run(and_(ANY(str), contains('setup.py bdist_wheel')))
    when(CTX.repo).get_current_branch().thenReturn('branch')
    when(epab.utils).get_next_version().thenReturn('next_version')

    expect(ctx).invoke(epab.cmd.pytest, long=True)
    expect(ctx).invoke(epab.linters.lint)
    expect(repo).push_tags()

    _release._release(ctx)

    verify(CTX.repo, atleast=1).is_dirty(untracked=True)
    verify(CTX.repo, atleast=1).get_current_branch()


def test_release_on_master():
    ctx = mock()
    repo = mock()
    CTX.repo = repo

    when(CTX.repo).get_current_branch().thenReturn('master')
    when(epab.utils).get_next_version().thenReturn('next_version')

    expect(ctx).invoke(epab.linters.lint)
    expect(ctx).invoke(epab.cmd.pytest, long=True)
    expect(elib_run).run(contains('python.exe setup.py bdist_wheel'))
    expect(elib_run).run(f'twine upload dist/* --skip-existing', mute=True)

    config.PACKAGE_NAME.default = 'test'
    epab.cmd._release._release(ctx)


def test_dirty_initial_check(caplog):
    ctx = mock()
    repo = mock()
    CTX.repo = repo

    when(epab.utils).get_next_version().thenReturn('next_version')
    when(CTX.repo).is_dirty(untracked=True).thenReturn(True)
    with pytest.raises(SystemExit):
        epab.cmd._release._release(ctx)
    assert 'initial check failed' in caplog.text


def test_dirty_after_lint(caplog):
    ctx = mock()
    repo = mock()
    CTX.repo = repo

    when(epab.utils).get_next_version().thenReturn('next_version')
    when(CTX.repo).is_dirty(untracked=True) \
        .thenReturn(False) \
        .thenReturn(True)

    with pytest.raises(SystemExit):
        epab.cmd._release._release(ctx)
    assert 'linters produced artifacts' in caplog.text


def test_dirty_final_check(caplog):
    ctx = mock()
    repo = mock()
    CTX.repo = repo

    when(epab.utils).get_next_version().thenReturn('next_version')
    when(CTX.repo).is_dirty(untracked=True) \
        .thenReturn(False) \
        .thenReturn(False) \
        .thenReturn(True)

    with pytest.raises(SystemExit):
        epab.cmd._release._release(ctx)
    assert 'repository is dirty: last check before build' in caplog.text


def test_cleanup():
    config.PACKAGE_NAME.default = 'package'
    _create_dummy_release_artifacts()
    for artifact in RELEASE_ARTIFACTS:
        assert Path(artifact).exists()
    epab.cmd._release._clean()
    for artifact in RELEASE_ARTIFACTS:
        assert not Path(artifact).exists()


def test_appveyor(monkeypatch):
    ctx = mock()
    repo = mock()
    CTX.repo = repo

    CTX.appveyor = True

    Path('appveyor.yml').touch()

    when(epab.utils).get_next_version().thenReturn('next_version')

    expect(elib_run).run('appveyor UpdateBuild -Version next_version-0001-ABCDEF')
    expect(elib_run).run(contains('python.exe setup.py bdist_wheel'))
    expect(elib_run).run('appveyor SetVariable -Name EPAB_VERSION -Value next_version')
    expect(subprocess, atleast=1).call(...)

    monkeypatch.setenv('APPVEYOR_REPO_BRANCH', 'branch')
    monkeypatch.setenv('APPVEYOR_BUILD_NUMBER', '0001')
    monkeypatch.setenv('APPVEYOR_REPO_COMMIT', 'ABCDEF')

    epab.cmd._release._release(ctx)

    assert not Path('appveyor.yml').exists()


def test_appveyor_artifacts(monkeypatch):
    ctx = mock()
    repo = mock()
    CTX.repo = repo

    config.PACKAGE_NAME.default = 'test'
    CTX.appveyor = True
    config.ARTIFACTS.default = ['./artifacts_src/*']

    Path('./artifacts_src').mkdir()
    test_file_1 = Path('./artifacts_src/test1').absolute()
    test_file_2 = Path('./artifacts_src/test2').absolute()
    test_file_3 = Path('./artifacts_src/test3').absolute()
    test_file_1.touch()
    test_file_2.touch()
    test_file_3.touch()

    when(epab.utils).get_next_version().thenReturn('next_version')

    expect(elib_run).run('appveyor UpdateBuild -Version next_version-0001-ABCDEF')
    expect(elib_run).run(contains('python.exe setup.py bdist_wheel'))
    expect(elib_run).run('appveyor SetVariable -Name EPAB_VERSION -Value next_version')
    expect(subprocess, atleast=1).call(...)
    expect(shutil, times=3).copy(...)

    monkeypatch.setenv('APPVEYOR_REPO_BRANCH', 'branch')
    monkeypatch.setenv('APPVEYOR_BUILD_NUMBER', '0001')
    monkeypatch.setenv('APPVEYOR_REPO_COMMIT', 'ABCDEF')

    epab.cmd._release._release(ctx)


def test_appveyor_no_artifacts(monkeypatch):
    ctx = mock()
    repo = mock()
    CTX.repo = repo

    CTX.appveyor = True

    when(epab.utils).get_next_version().thenReturn('next_version')

    expect(elib_run).run('appveyor UpdateBuild -Version next_version-0001-ABCDEF')
    expect(elib_run).run(contains('python.exe setup.py bdist_wheel'))
    expect(elib_run).run('appveyor SetVariable -Name EPAB_VERSION -Value next_version')
    expect(shutil, times=0).copy(...)
    expect(subprocess, atleast=1).call(...)

    monkeypatch.setenv('APPVEYOR_REPO_BRANCH', 'branch')
    monkeypatch.setenv('APPVEYOR_BUILD_NUMBER', '0001')
    monkeypatch.setenv('APPVEYOR_REPO_COMMIT', 'ABCDEF')

    epab.cmd._release._release(ctx)
