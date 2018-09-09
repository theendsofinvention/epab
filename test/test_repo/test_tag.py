# coding=utf-8
from pathlib import Path

import pytest
from git.exc import GitCommandError


def test_tag(repo):
    assert repo.get_latest_tag() is None
    assert not repo.is_on_tag()
    repo.tag('test')
    assert repo.get_latest_tag() == 'test'
    assert repo.is_on_tag()
    repo.remove_tag('test')
    assert repo.get_latest_tag() is None
    assert not repo.is_on_tag()


def test_get_current_tag(repo):
    assert repo.get_current_tag() is None
    repo.tag('test')
    assert repo.get_current_tag() == 'test'
    Path('test').touch()
    repo.commit('msg')
    assert repo.get_current_tag() is None


def test_existing_tag(repo):
    repo.tag('test')
    Path('test').touch()
    repo.commit('msg')
    assert repo.get_current_tag() is None
    with pytest.raises(GitCommandError):
        repo.tag('test')
    repo.tag('test', overwrite=True)
    assert repo.get_current_tag() == 'test'


def test_list_tags_no_tags(repo):
    list_of_tags = repo.list_tags()
    assert isinstance(list_of_tags, list)
    assert not list_of_tags


def test_list_tags(repo):
    repo.tag('test')
    list_of_tags = repo.list_tags()
    assert isinstance(list_of_tags, list)
    assert len(list_of_tags) == 1
    assert 'test' in list_of_tags


def test_list_of_tags_pattern(repo):
    repo.tag('test')
    repo.tag('moo')
    list_of_tags = repo.list_tags()
    assert isinstance(list_of_tags, list)
    assert len(list_of_tags) == 2
    assert 'test' in list_of_tags
    assert 'moo' in list_of_tags
    test_list = repo.list_tags('test')
    assert isinstance(test_list, list)
    assert len(test_list) == 1
    assert 'test' in test_list
    moo_list = repo.list_tags('moo')
    assert isinstance(moo_list, list)
    assert len(moo_list) == 1
    assert 'moo' in moo_list
    nope_list = repo.list_tags('nope')
    assert isinstance(nope_list, list)
    assert not nope_list
