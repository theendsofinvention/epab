# coding=utf-8

import os
import pathlib
import webbrowser
from pathlib import Path

import pytest
from mockito import verifyStubbedInvocationsAreUsed, when

import epab.cmd._pytest
import epab.utils
from epab.cmd._pytest import _Coverage, _pytest, pytest_options
from epab.core import CONFIG, CTX

DEFAULT_OPTS = dict(
    long=False,
    show=False,
    exitfirst=False,
    last_failed=False,
    failed_first=False,
)


def test_environ():
    when(epab.utils).run(f'pytest test {pytest_options()}')
    _pytest('test', **DEFAULT_OPTS)
    assert os.environ.get('PYTEST_QT_API') == 'pyqt5'
    verifyStubbedInvocationsAreUsed()


def test_coverage_config_creation():
    when(epab.utils).run(f'pytest test {pytest_options()}')
    when(_Coverage).remove_config_file()
    _pytest('test', **DEFAULT_OPTS)
    assert pathlib.Path('.coveragerc').exists()
    verifyStubbedInvocationsAreUsed()


def test_coverage_config_removal_despite_error():
    with pytest.raises(RuntimeError):
        when(epab.utils).run(f'pytest test {pytest_options()}').thenRaise(RuntimeError('test'))
        _pytest('test', **DEFAULT_OPTS)
    assert not pathlib.Path('.coveragerc').exists()
    verifyStubbedInvocationsAreUsed()


def test_cmd():
    when(epab.utils).run(f'pytest test {pytest_options()}')
    _pytest('test', **DEFAULT_OPTS)
    verifyStubbedInvocationsAreUsed()


def test_cmd_with_coverage(monkeypatch):
    CTX.appveyor = True
    monkeypatch.setenv('SCRUT_TOK', 'test')
    Path('coverage.xml').touch()
    when(epab.utils).run('appveyor AddMessage "Uploading coverage to Codacy" -Category Information', mute=True)
    when(epab.utils).run('appveyor AddMessage "Codacy coverage OK" -Category Information', mute=True)
    when(epab.utils).run(f'pytest test --long {pytest_options()}')
    when(epab.utils).run('pip install --upgrade codacy-coverage')
    when(epab.utils).run('python-codacy-coverage -r coverage.xml')
    _pytest('test', **DEFAULT_OPTS)
    verifyStubbedInvocationsAreUsed()


def test_cmd_with_coverage_no_xml(monkeypatch):
    CTX.appveyor = True
    monkeypatch.setenv('SCRUT_TOK', 'test')
    when(epab.utils).run(
        'appveyor AddMessage ""coverage.xml" not found, skipping codacy coverage" -Category Error',
        mute=True
    )
    when(epab.utils).run(f'pytest test --long {pytest_options()}')
    _pytest('test', **DEFAULT_OPTS)
    verifyStubbedInvocationsAreUsed()


def test_long():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'long': True})
    when(epab.utils).run(f'pytest test {pytest_options()} --long')
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_show():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'show': True})
    cov_file = pathlib.Path('./htmlcov/index.html').absolute()
    when(webbrowser).open(f'file://{cov_file}')
    when(epab.utils).run(f'pytest test {pytest_options()}')
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_config_exit_first():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'exitfirst': True})
    CONFIG.test__runner_options = ''
    when(epab.utils).run(f'pytest test {pytest_options()} --exitfirst')
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_config_last_failed():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'last_failed': True})
    CONFIG.test__runner_options = ''
    when(epab.utils).run(f'pytest test {pytest_options()} --last-failed')
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_config_failed_first():
    opts = dict(**DEFAULT_OPTS)
    opts.update({'failed_first': True})
    CONFIG.test__runner_options = ''
    when(epab.utils).run(f'pytest test {pytest_options()} --failed-first')
    _pytest('test', **opts)
    verifyStubbedInvocationsAreUsed()


def test_output(capsys):
    when(epab.utils).run(f'pytest test {pytest_options()}')
    _pytest('test', **DEFAULT_OPTS)
    out, err = capsys.readouterr()
    assert out == 'EPAB: RUN_ONCE: running _pytest\nEPAB: Running test suite\nEPAB: skipping coverage upload\n'
    assert err == ''
    verifyStubbedInvocationsAreUsed()


def test_output_on_appveyor(capsys):
    CTX.appveyor = True
    when(epab.utils, strict=False).run(f'pytest test --long {pytest_options()}')
    _pytest('test', **DEFAULT_OPTS)
    out, err = capsys.readouterr()
    assert 'RUN_ONCE: running _pytest' in out
    assert 'EPAB: Running test suite' in out
    assert 'EPAB: Error: "coverage.xml" not found, skipping codacy coverage' in out
    assert err == ''
    verifyStubbedInvocationsAreUsed()


def test_config_show():
    CONFIG.test__runner_options = '-s'
    when(epab.utils).run(f'pytest test -s {pytest_options()}')
    _pytest('test', **DEFAULT_OPTS)
    verifyStubbedInvocationsAreUsed()


def test_config_appveyor(monkeypatch):
    CONFIG.test__av_runner_options = '--long'
    when(epab.utils).run(...)
    _pytest('test', **DEFAULT_OPTS)
    monkeypatch.setenv('APPVEYOR', 'test')
    CTX.run_once = {}
    _pytest('test', **DEFAULT_OPTS)
    verifyStubbedInvocationsAreUsed()
