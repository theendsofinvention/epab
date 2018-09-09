# coding=utf-8
from pathlib import Path

import pytest


def test_checkout(repo):
    repo.checkout('master')
    assert repo.get_current_branch() == 'master'
    with pytest.raises(SystemExit):
        repo.checkout('develop')
    repo.create_branch('develop')
    repo.checkout('develop')
    assert repo.get_current_branch() == 'develop'


def test_checkout_dirty(repo):
    repo.create_branch_and_checkout('develop')
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('dirty')
    with pytest.raises(SystemExit):
        repo.checkout('master')
    assert repo.index_is_empty()
    repo.stage_all()
    assert not repo.index_is_empty()
    with pytest.raises(SystemExit):
        repo.checkout('master')


def test_checkout_dry(repo):
    repo.create_branch_and_checkout('develop')
    assert repo.get_current_branch() == 'develop'
    repo.checkout('master')
    assert repo.get_current_branch() == 'master'
