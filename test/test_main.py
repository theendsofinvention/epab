# coding=utf-8

import traceback

import elib_run
import pytest
from click.testing import CliRunner, Result
from mockito import mock, verify, when

import epab.utils
from epab import __version__
from epab.__main__ import cli
from epab.cmd import _chglog, _install_hooks, _pytest, _release, _reqs
from epab.core import CTX, config
from epab.linters import _flake8, _lint, _pep8, _pylint, _safety, _mypy, _bandit, _dead_fixtures


@pytest.fixture(name='setup')
def _setup():
    repo = mock()
    when(repo).ensure()
    when(repo).changed_files().thenReturn(list())
    when(elib_run).run(...).thenReturn(('', 0))
    when(epab.utils).Repo(...).thenReturn(repo)
    return CliRunner(), repo


def succesfull_run(result):
    assert isinstance(result, Result)
    if result.exc_info:
        if result.exc_info[0] is SystemExit and result.exit_code == 0:
            pass
        else:
            traceback.print_exception(*result.exc_info)
            assert not result.exception
    assert result.exit_code == 0
    return True


def succesfull_run2(command):
    runner, _ = _setup()
    result = runner.invoke(cli, [command])
    assert isinstance(result, Result)
    if result.exc_info:
        if result.exc_info[0] is SystemExit and result.exit_code == 0:
            pass
        else:
            traceback.print_exception(*result.exc_info)
            assert not result.exception, result.output
    assert result.exit_code == 0
    return True


@pytest.mark.parametrize('param', ['-v', '--version'])
def test_version(param, setup):
    runner, repo = setup
    result = runner.invoke(cli, [param])
    assert isinstance(result, Result)
    assert result.output == f'{__version__}\n'
    verify(repo, times=0).ensure()
    assert result.exit_code == 0
    assert not result.exception


@pytest.mark.parametrize('param', ['-nv', '--next-version'])
def test_next_version(param, setup):
    runner, repo = setup
    when(epab.utils).get_next_version()
    result = runner.invoke(cli, [param])
    assert isinstance(result, Result)
    assert result.exit_code == 0
    assert not result.exception
    verify(repo, times=0).ensure()
    verify(epab.utils).get_next_version()


def test_dirty(setup):
    runner, repo = setup
    when(repo).is_dirty().thenReturn(True)
    result = runner.invoke(cli, ['safety'])
    assert isinstance(result, Result)
    assert result.exception
    assert isinstance(result.exception, SystemExit)
    assert 'Repository is dirty' in result.output
    assert result.exit_code == -1
    result = runner.invoke(cli, ['-d', 'safety'])
    assert isinstance(result, Result)
    assert not result.exception
    assert result.exit_code == 0


def test_stash(setup):
    assert not CTX.stash
    runner, repo = setup
    when(repo).is_dirty().thenReturn(False)
    result = runner.invoke(cli, ['-s', 'safety'])
    assert isinstance(result, Result)
    assert not result.exception
    assert result.exit_code == 0
    assert CTX.stash


def test_no_stash(setup):
    assert not CTX.stash
    runner, repo = setup
    when(repo).is_dirty().thenReturn(False)
    result = runner.invoke(cli, ['safety'])
    assert isinstance(result, Result)
    assert not result.exception
    assert result.exit_code == 0
    assert not CTX.stash


def test_pep8():
    when(_pep8)._pep8(...)
    assert succesfull_run2('pep8')
    verify(_pep8)._pep8(...)


def test_flake8():
    when(_flake8)._flake8(...)
    assert succesfull_run2('flake8')
    verify(_flake8)._flake8(...)


# def test_sort():
#     when(_sort)._sort(...)
#     assert succesfull_run2('sort')
#     verify(_sort)._sort(...)


def test_pylint():
    when(_pylint)._pylint(...)
    assert succesfull_run2('pylint')
    verify(_pylint)._pylint(...)


def test_safety():
    when(_safety)._safety(...)
    assert succesfull_run2('safety')
    verify(_safety)._safety(...)


def test_lint():
    when(_lint)._lint(...)
    assert succesfull_run2('lint')
    verify(_lint)._lint(...)


def test_reqs():
    when(_reqs)._write_reqs(...)
    assert succesfull_run2('reqs')
    verify(_reqs)._write_reqs(...)


def test_mypy():
    when(_mypy)._mypy(...)
    assert succesfull_run2('mypy')
    verify(_mypy)._mypy(...)


def test_bandit():
    when(_bandit)._bandit(...)
    assert succesfull_run2('bandit')
    verify(_bandit)._bandit(...)


def test_reqs_changed(setup):
    runner, repo = setup

    when(repo).changed_files().thenReturn(['requirements.txt'])
    result = runner.invoke(cli, ['reqs'])
    assert result.exception
    assert result.exc_info[0] is SystemExit
    verify(repo).changed_files()

    when(repo).changed_files().thenReturn(['requirements-dev.txt'])
    result = runner.invoke(cli, ['reqs'])
    assert result.exception
    assert result.exc_info[0] is SystemExit
    verify(repo, times=2).changed_files()

    when(repo).changed_files().thenReturn(['requirementx.txt', 'requirements-dev.txt'])
    result = runner.invoke(cli, ['reqs'])
    assert result.exception
    assert result.exc_info[0] is SystemExit
    verify(repo, times=3).changed_files()


def test_release():
    when(_release)._release(...)
    assert succesfull_run2('release')
    verify(_release)._release(...)


def test_chglog():
    when(_chglog)._chglog(...)
    assert succesfull_run2('chglog')
    verify(_chglog)._chglog(...)


def test_chglog_changed(setup):
    runner, repo = setup

    when(repo).changed_files().thenReturn(['CHANGELOG.rst'])
    result = runner.invoke(cli, ['chglog'])
    assert result.exception
    assert result.exc_info[0] is SystemExit
    verify(repo).changed_files()


def test_pytest():
    when(_pytest)._pytest(...)
    assert succesfull_run2('pytest')
    verify(_pytest)._pytest(...)


def test_install_hooks():
    when(_install_hooks)._install_hooks(...)
    assert succesfull_run2('install_hooks')
    verify(_install_hooks)._install_hooks(...)


def test_dead_fixtures():
    when(_dead_fixtures)._pytest_dead_fixtures(...)
    assert succesfull_run2('pytest_dead_fixtures')
    verify(_dead_fixtures)._pytest_dead_fixtures(...)


def test_setup_config():
    with pytest.raises(FileNotFoundError):
        config.setup_config('0.0.1')
