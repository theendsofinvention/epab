# coding=utf-8
from pathlib import Path

from epab.core import CTX


def test_tag(repo):
    assert repo.get_latest_tag() is None
    assert not repo.is_on_tag()
    repo.tag('test')
    assert repo.get_latest_tag() == 'test'
    assert repo.is_on_tag()
    repo.remove_tag('test')
    assert repo.get_latest_tag() is None
    assert not repo.is_on_tag()


def test_tag_dry(repo):
    assert repo.get_latest_tag() is None
    CTX.dry_run = True
    assert not repo.is_on_tag()
    repo.tag('test')
    assert repo.get_latest_tag() is None
    assert not repo.is_on_tag()
    CTX.dry_run = False
    repo.tag('test')
    CTX.dry_run = True
    repo.remove_tag('test')
    assert repo.get_latest_tag() == 'test'
    assert repo.is_on_tag()


def test_get_current_tag(repo):
    assert repo.get_current_tag() is None
    repo.tag('test')
    assert repo.get_current_tag() == 'test'
    Path('test').touch()
    repo.commit('msg')
    assert repo.get_current_tag() is None
