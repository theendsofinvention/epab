# coding=utf-8

from pathlib import Path

import elib_run
import pytest
from mockito import mock, verify, when

import epab.utils
from epab.cmd import _reqs
from epab.core import CTX


@pytest.fixture(autouse=True, name='repo')
def _all():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    # when(epab.utils).ensure_exe(...)
    yield repo


def test_empty_requirements():
    reqs = Path('requirements.txt')
    reqs_dev = Path('requirements-dev.txt')
    assert not reqs.exists()
    assert not reqs_dev.exists()
    when(elib_run).run('pipenv lock -r', mute=True, filters='Courtesy Notice: ').thenReturn(('', 0))
    when(elib_run).run('pipenv lock -r -d', mute=True, filters='Courtesy Notice: ').thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(False, False)
    assert reqs.exists()
    assert reqs_dev.exists()
    assert not reqs.read_text()
    assert not reqs_dev.read_text()


def test_requirements_no_dev_packages():
    reqs = Path('requirements.txt')
    reqs_dev = Path('requirements-dev.txt')
    when(elib_run).run('pipenv lock -r', mute=True, filters='Courtesy Notice: ').thenReturn(('reqs==0.1.0', 0))
    when(elib_run).run('pipenv lock -r -d', mute=True, filters='Courtesy Notice: ').thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(False, False)
    assert reqs.exists()
    assert reqs_dev.exists()
    assert reqs.read_text() == 'reqs==0.1.0'
    assert not reqs_dev.read_text()


def test_requirements_with_dev_packages():
    reqs = Path('requirements.txt')
    reqs_dev = Path('requirements-dev.txt')
    when(elib_run).run('pipenv lock -r', mute=True, filters='Courtesy Notice: ') \
        .thenReturn(('bad line\nreqs==0.1.0', 0))
    when(elib_run).run('pipenv lock -r -d', mute=True, filters='Courtesy Notice: ') \
        .thenReturn(('bad line\nreqs==0.1.1', 0))
    epab.cmd._reqs._write_reqs(False, False)
    assert reqs.exists()
    assert reqs_dev.exists()
    assert reqs.read_text() == 'reqs==0.1.0'
    assert reqs_dev.read_text() == 'reqs==0.1.1'


# @pytest.mark.long
def test_requirements_run_invocation():
    when(elib_run).run('pipenv lock -r', mute=True, filters='Courtesy Notice: ').thenReturn(('reqs', 0))
    when(elib_run).run('pipenv lock -r -d', mute=True, filters='Courtesy Notice: ').thenReturn(('reqs', 0))
    epab.cmd._reqs._write_reqs()


def test_requirements_output(caplog):
    caplog.set_level(10)
    when(Path).write_text(...)
    when(elib_run).run(...).thenReturn(('', 0))
    _reqs._write_reqs()
    assert 'running: _write_reqs' in caplog.text
    assert 'writing requirements' in caplog.text
    assert 'writing: requirements.txt' in caplog.text
    assert 'writing: requirements-dev.txt' in caplog.text
    verify(Path, times=2).write_text(...)
    verify(elib_run, times=2).run(...)


def test_straight_commit(repo):
    files_to_add = ['Pipfile', 'requirements.txt', 'requirements-dev.txt']
    when(Path).write_text(...)
    when(elib_run).run(...).thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(amend=True)
    verify(repo).amend_commit(append_to_msg='update requirements [auto]', files_to_add=files_to_add)
    verify(Path, times=2).write_text(...)
    verify(elib_run, times=2).run(...)


def test_commit_amend(repo):
    files_to_add = ['Pipfile', 'requirements.txt', 'requirements-dev.txt']
    when(Path).write_text(...)
    when(elib_run).run(...).thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(stage=True)
    verify(repo).stage_subset(*files_to_add)
    verify(Path, times=2).write_text(...)
    verify(elib_run, times=2).run(...)


def test_flags_exclusion(repo):
    when(Path).write_text(...)
    when(elib_run).run(...).thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(amend=True, stage=True)
    verify(repo).amend_commit(...)
    verify(Path, times=2).write_text(...)
    verify(elib_run, times=2).run(...)
