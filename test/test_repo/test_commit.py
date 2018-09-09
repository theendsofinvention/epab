# coding=utf-8
from pathlib import Path

import git
import pytest
from hypothesis import given, settings, strategies as st


def _dummy_commit(repo):
    Path('caribou').touch()
    repo.commit('msg')
    assert repo.last_commit_msg() == 'msg'


@given(message=st.from_regex(r'^[a-zA-Z0-9_]{1,79}(\n\n[a-zA-Z0-9_]{1,300})?$'))
@settings(deadline=None)
def test_commit(repo, message):
    test_file = Path('./test')
    if test_file.exists():
        test_file.unlink()
    else:
        Path('./test').touch()
    repo.commit(message)
    assert repo.last_commit_msg() == message.rstrip()


def test_empty_commit_message(repo):
    Path('./test').touch()
    with pytest.raises(SystemExit):
        repo.commit('')


def test_empty_commit(repo):
    assert not git.Repo().index.diff(git.Repo().head.commit)
    with pytest.raises(SystemExit):
        repo.commit('commit msg')
    repo.commit('commit msg', allow_empty=True)


def test_commit_appveyor(repo, monkeypatch):
    monkeypatch.setenv('APPVEYOR', 'test')
    repo.commit('commit msg', allow_empty=True)
    assert repo.last_commit_msg() == 'commit msg [skip ci]'


def test_commit_subset(repo, file_set):
    assert not repo.changed_files()
    for file in file_set:
        assert str(file) in repo.untracked_files()

    first_file = str(file_set[0])
    rest = file_set[1:]
    repo.commit('test', files_to_add=[first_file])
    untracked_files = repo.untracked_files()
    assert untracked_files
    assert first_file not in untracked_files
    for other in rest:
        assert str(other) in untracked_files


def test_commit_amend_new_message(repo):
    _dummy_commit(repo)
    assert len(list(repo.repo.iter_commits())) == 2
    repo.amend_commit(new_message='amended commit')
    assert repo.last_commit_msg() == 'amended commit'
    assert len(list(repo.repo.iter_commits())) == 2


def test_commit_amend_append_message(repo):
    _dummy_commit(repo)
    assert len(list(repo.repo.iter_commits())) == 2
    repo.amend_commit(append_to_msg='amended commit')
    assert repo.last_commit_msg() == 'msg\n\namended commit'
    assert len(list(repo.repo.iter_commits())) == 2
    repo.amend_commit(append_to_msg='second amend')
    assert repo.last_commit_msg() == 'msg\n\namended commit\nsecond amend'
    assert len(list(repo.repo.iter_commits())) == 2


def test_commit_amend_with_tag(repo):
    _dummy_commit(repo)
    assert len(list(repo.repo.iter_commits())) == 2
    repo.tag('test')
    assert repo.get_current_tag() == 'test'
    assert repo.get_latest_tag() == 'test'
    assert repo.is_on_tag()
    repo.amend_commit(new_message='msg')
    assert repo.get_current_tag() == 'test'
    assert repo.get_latest_tag() == 'test'
    assert repo.is_on_tag()
    assert len(list(repo.repo.iter_commits())) == 2
    repo.amend_commit(append_to_msg='msg')


def test_amend_commit_add_files(repo):
    _dummy_commit(repo)
    assert len(list(repo.repo.iter_commits())) == 2
    Path('moo').touch()
    Path('pig').touch()
    assert repo.is_dirty(untracked=True)
    assert len(repo.untracked_files()) == 2
    repo.amend_commit(new_message='test', files_to_add='moo')
    assert repo.is_dirty(untracked=True)
    assert len(repo.untracked_files()) == 1
    assert 'pig' in repo.untracked_files()


def test_commit_amend_root_commit(repo):
    assert repo.last_commit_msg() == 'init commit'
    assert len(list(repo.repo.iter_commits())) == 1
    with pytest.raises(SystemExit):
        repo.amend_commit(new_message='amended commit')


def test_commit_amend_wrong_params(repo):
    with pytest.raises(SystemExit):
        repo.amend_commit(new_message='test', append_to_msg='test')
    with pytest.raises(SystemExit):
        repo.amend_commit()


def test_commit_amend_appveyor(repo, monkeypatch):
    _dummy_commit(repo)
    assert len(list(repo.repo.iter_commits())) == 2
    monkeypatch.setenv('APPVEYOR', 'test')
    repo.amend_commit(new_message='test')
    assert repo.last_commit_msg() == 'test [skip ci]'
    assert len(list(repo.repo.iter_commits())) == 2


def test_make_skip_ci_commit(repo):
    message = 'test'
    assert repo.add_skip_ci_to_commit_msg(message) == 'test [skip ci]'
    message = 'test\n\ncaribou'
    assert repo.add_skip_ci_to_commit_msg(message) == 'test [skip ci]\n\ncaribou'


def test__sanitize_amend_commit_message(repo):
    assert repo.last_commit_msg() == 'init commit'
    assert repo._sanitize_amend_commit_message(new_message='test') == 'test'
    assert repo._sanitize_amend_commit_message(append_to_msg='test') == 'init commit\n\ntest'
    assert repo._sanitize_amend_commit_message(
        previous_message='init commit\n\ntest',
        append_to_msg='test'
    ) == 'init commit\n\ntest'
    assert repo._sanitize_amend_commit_message(
        previous_message='init commit\n\ntest\n',
        append_to_msg='other test'
    ) == 'init commit\n\ntest\nother test'
    with pytest.raises(SystemExit):
        repo._sanitize_amend_commit_message()
