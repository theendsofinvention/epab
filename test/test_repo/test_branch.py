# coding=utf-8
import pytest


def test_list_branches(repo):
    assert repo.list_branches() == ['master']


def test_active_branch(repo):
    assert repo.get_current_branch() == 'master'


@pytest.mark.parametrize(
    'branch',
    ['develop', 'feature/test', 'release/0.1.0dev1', 'patch/2017.08.12']
)
def test_create_branch_and_checkout(repo, branch):
    with pytest.raises(SystemExit):
        repo.create_branch_and_checkout('master')
    repo.create_branch_and_checkout(branch)
    assert repo.get_current_branch() == branch
    assert branch in repo.list_branches()
    with pytest.raises(SystemExit):
        repo.create_branch_and_checkout(branch)


@pytest.mark.parametrize(
    'branch',
    ['white space', '.dot', 'slash/', 'plop.lock', 'te^st', 'te~st', 'te:st', 'back\slash']
)
def test_create_branch_invalid_name(repo, branch):
    with pytest.raises(SystemExit):
        repo.create_branch(branch)


def test_create_branch(repo):
    assert repo.get_current_branch() == 'master'
    repo.create_branch('develop')
    assert repo.get_current_branch() == 'master'
    assert 'develop' in repo.list_branches()
    repo.checkout('develop')
    assert repo.get_current_branch() == 'develop'
