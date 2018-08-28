# coding=utf-8

from pathlib import Path

import elib_run
import pytest
from mockito import mock, spy2, verify, when

import epab.cmd._reqs
import epab.utils
from epab.core import CTX


@pytest.fixture(autouse=True, name='repo')
def _all():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    when(epab.utils).ensure_exe(...)
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


def test_requirement_dry_run():
    CTX.dry_run = True
    reqs = Path('requirements.txt')
    reqs_dev = Path('requirements-dev.txt')
    epab.cmd._reqs._write_reqs(False, False)
    assert not reqs.exists()
    assert not reqs_dev.exists()


@pytest.mark.long
def test_requirements_run_invocation():
    spy2(epab.utils.error)
    when(elib_run).run(...).thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(False, False)
    verify(elib_run, times=2).run(...)
    when(elib_run).run('pipenv lock -r', mute=True, filters='Courtesy Notice: ').thenReturn(('reqs', 0))
    when(elib_run).run('pipenv lock -r -d', mute=True, filters='Courtesy Notice: ').thenReturn(('reqs', 0))
    epab.cmd._reqs._write_reqs(False, False)
    when(elib_run).run(...).thenReturn(('error', 1))


def test_requirements_output():
    spy2(epab.utils.info)
    spy2(epab.utils.error)
    when(elib_run).run(...).thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(False, False)
    verify(epab.utils).info('RUN_ONCE: running _write_reqs')
    epab.cmd._reqs._write_reqs(False, False)
    verify(epab.utils).info('RUN_ONCE: skipping _write_reqs')
    verify(epab.utils).info('Writing requirements')
    verify(epab.utils).info('Writing requirements.txt')
    verify(epab.utils).info('Writing requirements-dev.txt')
    verify(epab.utils, times=5).info(...)
    verify(epab.utils, times=0).error(...)
    when(elib_run).run(...).thenReturn(('error', 1))


def test_straight_commit(repo):
    files_to_add = ['Pipfile', 'requirements.txt', 'requirements-dev.txt']
    when(elib_run).run(...).thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(amend=True, stage=False)
    verify(repo).amend_commit(append_to_msg='update requirements [auto]', files_to_add=files_to_add)


def test_commit_amend(repo):
    files_to_add = ['Pipfile', 'requirements.txt', 'requirements-dev.txt']
    when(elib_run).run(...).thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(amend=False, stage=True)
    verify(repo).stage_subset(*files_to_add)


def test_flags_exclusion(repo):
    when(elib_run).run(...).thenReturn(('', 0))
    epab.cmd._reqs._write_reqs(amend=True, stage=True)
    verify(repo).amend_commit(...)
