# coding=utf-8
import shutil
from pathlib import Path

import elib_run
import pytest
from mockito import ANY, and_, contains, mock, verify, verifyNoUnwantedInteractions, when, verifyStubbedInvocationsAreUsed

import epab.cmd
import epab.cmd._release
import epab.linters
import epab.utils
from epab.core import CTX, config


@pytest.fixture(autouse=True, name='setup')
def _all():
    ctx = mock()
    repo = mock()
    CTX.repo = repo
    when(ctx).invoke(...)
    when(CTX.repo).get_current_branch().thenReturn('branch')
    when(epab.utils).get_next_version().thenReturn('next_version')
    when(CTX.repo).is_dirty(untracked=True).thenReturn(False)
    when(CTX.repo).tag(...)
    when(CTX.repo).remove_tag(...)
    when(CTX.repo).commit(...)
    when(CTX.repo).push(...)
    when(elib_run).run(...)
    yield ctx, repo


RELEASE_ARTIFACTS = ['.eggs', 'build', 'package.egg-info']


def _create_dummy_release_artifacts():
    Path('.eggs').mkdir()
    Path('build').mkdir()
    Path('package.egg-info').mkdir()


def test_release(setup):
    ctx, repo = setup

    epab.cmd._release._release(ctx)

    verify(repo).get_current_branch()
    when(epab.utils).get_next_version()
    verify(CTX.repo, times=3).is_dirty(untracked=True)
    verify(ctx).invoke(epab.linters.lint)
    verify(ctx).invoke(epab.cmd.pytest, long=True)
    # verify(ctx).invoke(epab.cmd.reqs)
    verify(repo).tag('next_version', overwrite=True)
    # verify(ctx).invoke(epab.cmd.chglog, next_version='next_version')
    verify(elib_run).run(and_(ANY(str), contains('setup.py bdist_wheel')))
    verifyNoUnwantedInteractions(epab.utils)
    verify(repo).push_tags(...)
    verifyNoUnwantedInteractions(repo)


def test_release_on_master(setup):
    ctx, repo = setup
    when(CTX.repo).get_current_branch().thenReturn('master')
    config.PACKAGE_NAME.default = 'test'
    epab.cmd._release._release(ctx)

    verify(repo).get_current_branch()
    when(epab.utils).get_next_version()
    verify(CTX.repo, times=3).is_dirty(untracked=True)
    verify(ctx).invoke(epab.linters.lint)
    verify(ctx).invoke(epab.cmd.pytest, long=True)
    # verify(ctx).invoke(epab.cmd.reqs)
    verify(repo).tag('next_version', overwrite=True)
    # verify(ctx).invoke(epab.cmd.chglog, next_version='next_version')
    verify(elib_run).run(and_(ANY(str), contains('setup.py bdist_wheel')))
    verify(elib_run).run(
        f'twine upload dist/* --skip-existing',
        mute=True
    )
    verifyNoUnwantedInteractions(repo)


def test_dirty_initial_check(setup):
    ctx, _ = setup
    when(epab.utils.AV).error(...)
    when(CTX.repo).changed_files().thenReturn(list())
    when(CTX.repo).is_dirty(untracked=True).thenReturn(True)
    with pytest.raises(SystemExit):
        epab.cmd._release._release(ctx)
    verify(epab.utils.AV).error('Repository is dirty', 'initial check failed')


def test_dirty_after_lint(setup):
    ctx, _ = setup
    when(epab.utils.AV).error(...)
    when(CTX.repo).changed_files().thenReturn(list())
    when(CTX.repo).is_dirty(untracked=True) \
        .thenReturn(False) \
        .thenReturn(True)
    with pytest.raises(SystemExit):
        epab.cmd._release._release(ctx)
    verify(epab.utils.AV).error('Repository is dirty', 'linters produced artifacts')


def test_dirty_final_check(setup):
    ctx, _ = setup
    when(CTX.repo).changed_files().thenReturn(list())
    when(epab.utils.AV).error(...)
    when(CTX.repo).is_dirty(untracked=True) \
        .thenReturn(False) \
        .thenReturn(False) \
        .thenReturn(True)
    with pytest.raises(SystemExit):
        epab.cmd._release._release(ctx)
    verify(epab.utils.AV).error('Repository is dirty', 'last check before build')


def test_dry(setup, capsys):
    ctx, _ = setup
    CTX.dry_run = True
    epab.cmd._release._release(ctx)
    out, _ = capsys.readouterr()
    assert 'Skipping release; DRY RUN' in out


def test_cleanup():
    config.PACKAGE_NAME.default = 'package'
    _create_dummy_release_artifacts()
    for artifact in RELEASE_ARTIFACTS:
        assert Path(artifact).exists()
    CTX.dry_run = True
    epab.cmd._release._clean()
    for artifact in RELEASE_ARTIFACTS:
        assert Path(artifact).exists()
    CTX.dry_run = False
    epab.cmd._release._clean()
    for artifact in RELEASE_ARTIFACTS:
        assert not Path(artifact).exists()


def test_appveyor(setup, monkeypatch):
    Path('appveyor.yml').touch()
    ctx, _ = setup
    CTX.appveyor = True
    monkeypatch.setenv('APPVEYOR_REPO_BRANCH', 'branch')
    monkeypatch.setenv('APPVEYOR_BUILD_NUMBER', '0001')
    monkeypatch.setenv('APPVEYOR_REPO_COMMIT', 'ABCDEF')
    epab.cmd._release._release(ctx)
    verify(elib_run).run('appveyor UpdateBuild -Version next_version-0001-ABCDEF')
    assert not Path('appveyor.yml').exists()


def test_appveyor_artifacts(setup, monkeypatch):
    config.PACKAGE_NAME.default = 'test'
    ctx, _ = setup
    CTX.appveyor = True
    when(shutil).copy(...)
    Path('./artifacts_src').mkdir()
    test_file_1 = Path('./artifacts_src/test1').absolute()
    test_file_2 = Path('./artifacts_src/test2').absolute()
    test_file_3 = Path('./artifacts_src/test3').absolute()
    test_file_1.touch()
    test_file_2.touch()
    test_file_3.touch()
    config.ARTIFACTS.default = ['./artifacts_src/*']
    monkeypatch.setenv('APPVEYOR_REPO_BRANCH', 'branch')
    monkeypatch.setenv('APPVEYOR_BUILD_NUMBER', '0001')
    monkeypatch.setenv('APPVEYOR_REPO_COMMIT', 'ABCDEF')
    epab.cmd._release._release(ctx)
    verify(elib_run).run('appveyor UpdateBuild -Version next_version-0001-ABCDEF')
    verify(shutil).copy(str(test_file_1), str(Path('./artifacts').absolute()))
    verify(shutil).copy(str(test_file_2), str(Path('./artifacts').absolute()))
    verify(shutil).copy(str(test_file_3), str(Path('./artifacts').absolute()))


def test_appveyor_no_artifacts(setup, monkeypatch):
    ctx, _ = setup
    CTX.appveyor = True
    when(shutil).copy(...)
    when(epab.utils.AV).info(...)
    monkeypatch.setenv('APPVEYOR_REPO_BRANCH', 'branch')
    monkeypatch.setenv('APPVEYOR_BUILD_NUMBER', '0001')
    monkeypatch.setenv('APPVEYOR_REPO_COMMIT', 'ABCDEF')
    epab.cmd._release._release(ctx)
    verify(shutil, times=0).copy(...)
