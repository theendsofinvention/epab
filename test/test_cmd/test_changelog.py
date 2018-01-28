# coding=utf-8

from pathlib import Path

import pytest
from mockito import mock, verify, when

import epab.utils
# noinspection PyProtectedMember
from epab.cmd._chglog import _chglog
from epab.core import CONFIG, CTX


@pytest.fixture(autouse=True, name='repo')
def _all():
    repo = mock(spec=epab.utils.Repo)
    when(epab.utils).run(...).thenReturn(('', 0))
    CTX.repo = repo
    when(epab.utils).ensure_exe(...)
    yield repo


def test_changelog_config_disabled():
    changelog = Path('CHANGELOG.rst')
    Path('epab.yml').write_text('changelog:\n  disable: true\npackage: test')
    CONFIG.load()
    assert CONFIG.changelog__disable is True
    when(epab.utils).info(...)
    when(epab.utils).run('gitchangelog', mute=True).thenReturn('content', 0)
    _chglog(False, False)
    verify(epab.utils).info('Skipping changelog update as per config')
    assert not changelog.exists()


@pytest.mark.parametrize(
    'src,result',
    [
        ('content', 'content'),
        ('content    \r\n\r\ncontent', 'content    \n\n\n\ncontent'),
        ('content  \r\n\r\n\r\ncontent', 'content  \n\n\n\n\n\ncontent'),

    ]
)
def test_changelog(src, result):
    changelog = Path('CHANGELOG.rst')
    CONFIG.load()
    assert not CONFIG.changelog__disable
    when(epab.utils).ensure_exe(...)
    when(epab.utils).info(...)
    when(epab.utils).run('gitchangelog', mute=True).thenReturn((src, 0))
    _chglog(False, False)
    verify(epab.utils).info('Writing changelog')
    assert changelog.exists()
    assert changelog.read_text() == result


def test_straight_commit(repo):
    _chglog(True, False)
    verify(repo).amend_commit(append_to_msg='update changelog [auto]', files_to_add=CONFIG.changelog__file)


def test_commit_amend(repo):
    _chglog(amend=False, stage=True)
    verify(repo).stage_subset(CONFIG.changelog__file)


def test_flags_exclusion(repo):
    _chglog(amend=True, stage=True)
    verify(repo).amend_commit(...)


def test_next_version(repo):
    _chglog(next_version='test')
    verify(repo).tag('test')
    verify(repo).remove_tag('test')


def test_auto_next_version():
    when(epab.utils).get_git_version_info().thenReturn('test')
    _chglog(auto_next_version=True)
    verify(epab.utils).get_git_version_info()
