# coding=utf-8
from pathlib import Path

import pytest


def test_merge(repo):
    repo.create_branch_and_checkout('develop')
    Path('test').touch()
    repo.commit('test')
    sha = repo.get_sha()
    short_sha = repo.get_short_sha()
    repo.checkout('master')
    repo.merge('develop')
    assert sha == repo.get_sha()
    assert short_sha == repo.get_short_sha()


def test_merge_dry_run(repo):
    repo.create_branch_and_checkout('develop')
    Path('test').touch()
    repo.commit('test')
    sha = repo.get_sha()
    repo.checkout('master')


def test_merge_dirty(repo):
    Path('test').write_text('clean')
    assert 'test' in repo.untracked_files()
    repo.commit('test')
    repo.create_branch_and_checkout('develop')
    repo.checkout('master')
    Path('test').write_text('dirty')
    with pytest.raises(SystemExit):
        repo.merge('develop')
