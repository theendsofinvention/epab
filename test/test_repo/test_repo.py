# coding=utf-8

import os
from pathlib import Path

import pytest

import epab.utils


def test_ensure(repo):
    subdir = Path('./test').absolute()
    subdir.mkdir()
    os.chdir(str(subdir))
    with pytest.raises(SystemExit):
        repo.ensure()


def test_git_init(repo):
    assert Path('.git').exists()
    assert repo.get_current_branch() == 'master'
    repo.ensure()


def test_push(dummy_git_repo):
    origin_path = Path('./origin').absolute()
    origin_path.mkdir()
    fork_path = Path('./fork').absolute()
    fork_path.mkdir()
    os.chdir(origin_path)
    dummy_git_repo.create()
    origin_repo = epab.utils.Repo()
    origin_repo.repo.clone(f'{fork_path}')
    os.chdir(fork_path)
    fork_repo = epab.utils.Repo()
    assert fork_repo.get_sha() == origin_repo.get_sha()
    Path('caribou').touch()
    fork_repo.commit('msg')
    assert fork_repo.get_sha() != origin_repo.get_sha()
    origin_repo.create_branch_and_checkout('develop')
    fork_repo.push()
    origin_repo.checkout('master')
    assert fork_repo.get_sha() == origin_repo.get_sha()


def test_list_of_untracked_files(repo, file_set):
    assert not repo.changed_files()
    untracked_files = repo.untracked_files()
    for file in file_set:
        assert str(file) in untracked_files


def test_list_of_changed_files(repo, file_set):
    assert not repo.changed_files()
    assert not repo.changed_files()
    assert len(repo.untracked_files()) == len(file_set)

    repo.commit('test')
    assert not repo.changed_files()
    assert not repo.untracked_files()

    file_set[0].write_text('moo')
    assert str(file_set[0]) in repo.changed_files()

    repo.commit('test', files_to_add=str(file_set[0]))
    assert not repo.changed_files()


def test_dirty_repo(repo):
    assert not repo.is_dirty()
    file = Path('test')
    file.touch()
    assert repo.is_dirty(untracked=True)
    assert not repo.is_dirty()
    repo.commit('test')
    assert not repo.is_dirty(untracked=True)
    assert not repo.is_dirty()
    file.write_text('moo')
    assert repo.is_dirty(untracked=True)
    assert repo.is_dirty()
    repo.stage_all()
    assert repo.is_dirty(untracked=True)
    assert repo.is_dirty()


def test_status(repo):
    assert not repo.is_dirty()
    assert 'nothing to commit' in repo.status()
    Path('test').touch()
    assert 'untracked files present' in repo.status()
    repo.stage_all()
    assert 'new file:   test' in repo.status()
    repo.commit('test')
    assert 'nothing to commit' in repo.status()
