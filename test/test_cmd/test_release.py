# coding=utf-8
import os
from pathlib import Path

import pytest
from mockito import ANY, and_, contains, mock, verify, when

import epab.cmd
import epab.cmd._release
import epab.linters
import epab.utils
from epab.core import CONFIG, CTX


@pytest.fixture(autouse=True, name='setup')
def _all():
    ctx = mock()
    repo = mock()
    CTX.repo = repo
    when(ctx).invoke(...)
    when(CTX.repo).get_current_branch().thenReturn('branch')
    when(epab.utils).get_git_version_info().thenReturn('next_version')
    when(CTX.repo).is_dirty(untracked=True).thenReturn(False)
    when(CTX.repo).tag(...)
    when(CTX.repo).remove_tag(...)
    when(CTX.repo).commit(...)
    when(CTX.repo).push(...)
    when(epab.utils).run(...)
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
    when(epab.utils).get_git_version_info()
    verify(CTX.repo, times=2).is_dirty(untracked=True)
    verify(ctx).invoke(epab.linters.lint)
    verify(ctx).invoke(epab.cmd.pytest, long=True)
    verify(ctx).invoke(epab.cmd.reqs, stage=True)
    verify(repo, times=1).tag('next_version')
    verify(ctx).invoke(epab.cmd.chglog, stage=True, next_version='next_version')
    verify(epab.utils).run(and_(ANY(str), contains('setup.py sdist bdist_wheel')))
    verify(epab.utils).run(
        f'twine upload dist/* --skip-existing',
        mute=True
    )
    verify(repo).push(...)


def test_dirty(setup):
    ctx, repo = setup
    when(CTX.repo).is_dirty(untracked=True).thenReturn(True)
    with pytest.raises(SystemExit):
        epab.cmd._release._release(ctx)


def test_dry(setup, capsys):
    ctx, repo = setup
    CTX.dry_run = True
    epab.cmd._release._release(ctx)
    out, _ = capsys.readouterr()
    assert 'Skipping release; DRY RUN' in out


def test_cleanup():
    CONFIG.package = 'package'
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


def test_appveyor(setup):
    ctx, _ = setup
    CTX.appveyor = True
    os.environ['APPVEYOR_REPO_BRANCH'] = 'branch'
    os.environ['APPVEYOR_BUILD_NUMBER'] = '0001'
    os.environ['APPVEYOR_REPO_COMMIT'] = 'ABCDEF'
    epab.cmd._release._release(ctx)
    verify(epab.utils).run('appveyor UpdateBuild -Version next_version-0001-ABCDEF')
    verify(epab.utils).run('pip install --upgrade codacy-coverage')
    verify(epab.utils).run('python-codacy-coverage -r coverage.xml')
