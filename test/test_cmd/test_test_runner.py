# coding=utf-8

import os
import pathlib
import subprocess
import webbrowser
from pathlib import Path

import elib_run
import pytest
from mockito import verifyStubbedInvocationsAreUsed, when

from epab._logging import _setup_logging
from epab.cmd._pytest import _Coverage, _pytest, pytest_options
from epab.core import CTX, config

DEFAULT_OPTS = dict(
    long=False,
    show=False,
    exitfirst=False,
    last_failed=False,
    failed_first=False,
    rm_cov=False,
)

_TIMEOUT = config.TEST_PYTEST_TIMEOUT()


def test_environ():
    when(elib_run).run(f'pytest test {pytest_options()}', timeout=_TIMEOUT)
    _pytest('test', **DEFAULT_OPTS)
    assert os.environ.get('PYTEST_QT_API') == 'pyqt5'
    verifyStubbedInvocationsAreUsed()


def test_coverage_config_creation():
    when(elib_run).run(f'pytest test {pytest_options()}', timeout=_TIMEOUT)
    when(_Coverage).remove_config_file()
    _pytest('test', **DEFAULT_OPTS)
    assert pathlib.Path('.coveragerc').exists()
    verifyStubbedInvocationsAreUsed()


def test_coverage_config_removal_despite_error():
    with pytest.raises(RuntimeError):
        when(elib_run).run(f'pytest test {pytest_options()}', timeout=_TIMEOUT).thenRaise(RuntimeError('test'))
        _pytest('test', **DEFAULT_OPTS)
    assert not pathlib.Path('.coveragerc').exists()
    verifyStubbedInvocationsAreUsed()


def test_cmd():
    when(elib_run).run(f'pytest test {pytest_options()}', timeout=_TIMEOUT)
    _pytest('test', **DEFAULT_OPTS)
    verifyStubbedInvocationsAreUsed()


def test_cmd_with_coverage(monkeypatch, caplog):
    caplog.set_level(10)
    CTX.appveyor = True
    monkeypatch.setenv('SCRUT_TOK', 'test')
    monkeypatch.setenv('CODACY_PROJECT_TOKEN', 'test')
    Path('coverage.xml').touch()
    when(subprocess).call(...)
    when(elib_run).run(f'pytest test --vcr-record=none --long {pytest_options()}', timeout=_TIMEOUT)
    when(elib_run).run('pip install --upgrade codacy-coverage')
    when(elib_run).run('python-codacy-coverage -r coverage.xml')
    _pytest('test', **DEFAULT_OPTS)
    assert 'uploading coverage to Codacy' in caplog.text
    assert 'codacy coverage OK' in caplog.text


def test_cmd_with_coverage_no_xml(monkeypatch, caplog):
    _setup_logging()
    CTX.appveyor = True
    monkeypatch.setenv('SCRUT_TOK', 'test')
    when(subprocess).call(...)
    when(elib_run).run(f'pytest test --vcr-record=none --long {pytest_options()}', timeout=_TIMEOUT)
    _pytest('test', **DEFAULT_OPTS)
    assert 'coverage.xml not found, skipping codacy coverage' in caplog.text


def test_long():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'long': True})
    when(elib_run).run(f'pytest test {pytest_options()} --long', timeout=_TIMEOUT)
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_show():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'show': True})
    cov_file = pathlib.Path('./htmlcov/index.html').absolute()
    when(webbrowser).open(f'file://{cov_file}')
    when(elib_run).run(f'pytest test {pytest_options()}', timeout=_TIMEOUT)
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_config_exit_first():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'exitfirst': True})
    when(elib_run).run(f'pytest test {pytest_options()} --exitfirst', timeout=_TIMEOUT)
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_config_last_failed():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'last_failed': True})
    when(elib_run).run(f'pytest test {pytest_options()} --last-failed', timeout=_TIMEOUT)
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_config_failed_first():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'failed_first': True})
    when(elib_run).run(f'pytest test {pytest_options()} --failed-first', timeout=_TIMEOUT)
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_output(capsys, caplog):
    caplog.set_level(10)
    when(elib_run).run(f'pytest test {pytest_options()}', timeout=_TIMEOUT)
    _pytest('test', **DEFAULT_OPTS)
    out, err = capsys.readouterr()
    assert 'running: _pytest' in caplog.text
    assert 'running test suite' in caplog.text
    assert 'skipping coverage upload' in caplog.text
    # assert 'running _pytest\nEPAB: Running test suite\nEPAB: skipping coverage upload\n' in out
    assert err == ''


def test_output_on_appveyor(caplog):
    CTX.appveyor = True
    when(subprocess).call(...)
    when(elib_run, strict=False).run(f'pytest test --vcr-record=none --long {pytest_options()}', timeout=_TIMEOUT)
    _pytest('test', **DEFAULT_OPTS)
    assert 'running: _pytest' in caplog.text
    assert 'running test suite' in caplog.text
    assert 'coverage.xml not found, skipping codacy coverage' in caplog.text


def test_config_show():
    config.TEST_RUNNER_OPTIONS.default = '-s'
    when(elib_run).run(f'pytest test -s {pytest_options()}', timeout=_TIMEOUT)
    _pytest('test', **DEFAULT_OPTS)


def test_config_appveyor(monkeypatch):
    when(elib_run).run(...)
    _pytest('test', **DEFAULT_OPTS)
    monkeypatch.setenv('APPVEYOR', 'test')
    CTX.run_once = {}
    _pytest('test', **DEFAULT_OPTS)


def test_remove_coverage_dir_disabled():
    CTX.appveyor = False
    when(elib_run).run(...)
    cov_dir = Path('./htmlcov')
    assert not cov_dir.exists()
    cov_dir.mkdir()
    assert cov_dir.exists()
    _pytest('test', **DEFAULT_OPTS)


def test_remove_coverage():
    CTX.appveyor = False
    when(elib_run).run(...)
    cov_dir = Path('./htmlcov')
    assert not cov_dir.exists()
    cov_dir.mkdir()
    assert cov_dir.exists()
    new_opts = DEFAULT_OPTS.copy()
    new_opts.update({'rm_cov': True})
    _pytest('test', **new_opts)
    assert not cov_dir.exists()
