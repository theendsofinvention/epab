# coding=utf-8

from pathlib import Path

import elib_run
import pytest
from mockito import expect, mock, verify, when

import epab.utils
# noinspection PyProtectedMember
from epab.cmd._chglog import _chglog
from epab.core import CTX, config


# @pytest.fixture(autouse=True, name='repo')
# def _all():
#     repo = mock(spec=epab.utils.Repo)
#     when(elib_run).run(...).thenReturn(('', 0))
#     CTX.repo = repo
#     when(epab.utils).ensure_exe(...)
#     yield repo


def test_changelog_config_disabled(caplog):
    caplog.set_level(10)
    changelog = Path('CHANGELOG.md')
    config.CHANGELOG_DISABLE.default = True
    assert config.CHANGELOG_DISABLE() is True
    expect(elib_run, times=0).run(...)
    _chglog()
    assert 'skipping changelog update as per config' in caplog.text
    assert not changelog.exists()


@pytest.mark.parametrize(
    'src,result',
    [
        ('content', 'content'),
        ('content    \r\n\r\ncontent', 'content    \n\n\n\ncontent'),
        ('content  \r\n\r\n\r\ncontent', 'content  \n\n\n\n\n\ncontent'),

    ]
)
def test_changelog(src, result, caplog):
    caplog.set_level(10)
    changelog = Path('CHANGELOG.md')
    assert config.CHANGELOG_DISABLE() is False
    when(epab.utils).ensure_exe(...)
    when(elib_run).run('gitchangelog', mute=True).thenReturn((src, 0))
    _chglog()
    assert 'writing changelog' in caplog.text
    assert changelog.exists()
    assert changelog.read_text() == result


def test_straight_commit():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    when(epab.utils).ensure_exe(...)
    when(elib_run).run(...).thenReturn(('', 0))
    when(repo).amend_commit(append_to_msg='update changelog [auto]', files_to_add=str(config.CHANGELOG_FILE_PATH()))
    _chglog(True)


def test_commit_amend():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    when(epab.utils).ensure_exe(...)
    when(elib_run).run(...).thenReturn(('', 0))
    when(repo).stage_subset(str(config.CHANGELOG_FILE_PATH()))
    _chglog(stage=True)


def test_flags_exclusion():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    when(epab.utils).ensure_exe(...)
    when(elib_run).run(...).thenReturn(('', 0))
    when(repo).amend_commit(...)
    _chglog(amend=True, stage=True)


def test_next_version():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    when(epab.utils).ensure_exe(...)
    when(elib_run).run(...).thenReturn(('', 0))
    when(repo).tag('test')
    when(repo).remove_tag('test')
    _chglog(next_version='test')


def test_auto_next_version():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    when(epab.utils).ensure_exe(...)
    when(elib_run).run(...).thenReturn(('', 0))
    when(epab.utils).get_next_version().thenReturn('test')
    _chglog(auto_next_version=True)
    verify(epab.utils).get_next_version()
