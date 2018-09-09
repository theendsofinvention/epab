# coding=utf-8

from pathlib import Path

import pytest
from mockito import expect, mock, verify, verifyZeroInteractions, when

import epab.utils
from epab.core import CTX


def test_stash(repo):
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('test')
    assert 'test' in repo.changed_files()
    repo.stash('test')
    assert not repo.changed_files()


def test_unstash(repo):
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('test')
    assert 'test' in repo.changed_files()
    repo.stash('test')
    assert not repo.changed_files()
    repo.unstash()
    assert 'test' in repo.changed_files()


def test_stash_decorator():
    CTX.repo = mock()
    CTX.repo.stashed = False

    @epab.utils.stashed
    def _func():
        pass

    CTX.stash = True
    when(CTX.repo).stash(...)
    _func()
    verify(CTX.repo).stash(...)


def test_stash_decorator_disabled():
    CTX.repo = mock()
    CTX.stash = False

    @epab.utils.stashed
    def _func():
        pass

    expect(CTX.repo, times=0).stash(...)
    _func()
    verifyZeroInteractions(CTX.repo)


def test_stash_untracked_files(repo):
    Path('test').touch()
    with pytest.raises(SystemExit):
        repo.stash('test')


def test_stash_modified_index(repo):
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('test')
    repo.stage_all()
    with pytest.raises(SystemExit):
        repo.stash('test')


def test_already_stashed(repo):
    repo.stashed = True
    with pytest.raises(SystemExit):
        repo.stash('test')
