# coding=utf-8

import traceback

import pytest
from click.testing import CliRunner, Result
from mockito import expect, mock, unstub, verify, when

import epab.utils
from epab import __version__
from epab.__main__ import cli
# noinspection PyProtectedMember
from epab.cmd import _chglog, _install_hooks, _pytest, _release, _reqs
from epab.core import CTX, config
# noinspection PyProtectedMember
from epab.linters import _bandit, _dead_fixtures, _flake8, _lint, _mypy, _pep8, _pylint, _safety


def _succesfull_run(result):
    assert isinstance(result, Result)
    if result.exc_info:
        if result.exc_info[0] is SystemExit and result.exit_code == 0:
            return True

        traceback.print_exception(*result.exc_info)
        assert not result.exception

    assert result.exit_code == 0
    return True


def _succesfull_run2(command):
    runner, _ = _setup()
    result = runner.invoke(cli, [command])
    return _succesfull_run(result)


def _check_runner_result(cmd):
    runner = CliRunner()
    result = runner.invoke(cli, cmd)
    assert isinstance(result, Result)
    assert 0 == result.exit_code
    assert not result.exception


@pytest.mark.parametrize('param', ['-v', '--version'])
def test_version(param):
    repo = mock()
    runner = CliRunner()
    result = runner.invoke(cli, [param])
    assert isinstance(result, Result)
    assert result.output == f'{__version__}\n'
    verify(repo, times=0).ensure()
    assert result.exit_code == 0
    assert not result.exception


@pytest.mark.parametrize('param', ['-nv', '--next-version'])
def test_next_version(param):
    unstub()
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(epab.utils).get_next_version()
    _check_runner_result([param])
    verify(repo, times=0).ensure()


def test_dirty():
    repo = mock()
    runner = CliRunner()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
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


def test_stash_safety():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    assert not CTX.stash
    when(repo).is_dirty().thenReturn(False)
    _check_runner_result(['-s', 'safety'])
    assert CTX.stash


def test_no_stash():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(repo).is_dirty().thenReturn(False)
    assert not CTX.stash
    _check_runner_result(['safety'])
    assert not CTX.stash


# def test_pep8():
#     repo = mock()
#     when(repo).ensure()
#     when(epab.utils).Repo(...).thenReturn(repo)
#     when(repo).is_dirty().thenReturn(False)
#     when(_pep8)._pep8(...)
#     _check_runner_result(['pep8'])


def test_flake8():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(repo).is_dirty().thenReturn(False)
    when(_flake8)._flake8(...)
    _check_runner_result(['flake8'])


# def test_sort():
#     when(_sort)._sort(...)
#     assert _succesfull_run2('sort')
#     verify(_sort)._sort(...)


def test_pylint():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(repo).is_dirty().thenReturn(False)
    when(_pylint)._pylint(...)
    _check_runner_result(['pylint'])


def test_safety():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(repo).is_dirty().thenReturn(False)
    when(_safety)._safety(...)
    _check_runner_result(['safety'])


def test_lint():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(repo).is_dirty().thenReturn(False)
    when(_lint)._lint(...)
    _check_runner_result(['lint'])


def test_reqs():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(repo).changed_files().thenReturn(list())
    when(_reqs)._write_reqs(...)
    _check_runner_result(['reqs'])


def test_mypy():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(_mypy)._mypy(...)
    _check_runner_result(['mypy'])


def test_bandit():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(_bandit)._bandit(...)
    _check_runner_result(['bandit'])


def test_reqs_changed():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    runner = CliRunner()

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
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(_release)._release(...)
    _check_runner_result(['release'])


def test_chglog():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(repo).changed_files().thenReturn(list())
    when(_chglog)._chglog(...)
    _check_runner_result(['chglog'])


def test_chglog_changed():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    expect(_chglog, times=0)._chglog(...)
    runner = CliRunner()

    when(repo).changed_files().thenReturn(['CHANGELOG.rst'])
    result = runner.invoke(cli, ['chglog'])
    assert result.exception
    assert result.exc_info[0] is SystemExit
    verify(repo).changed_files()


def test_pytest():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(_pytest)._pytest(...)
    _check_runner_result(['pytest'])


def test_install_hooks():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(_install_hooks)._install_hooks(...)
    _check_runner_result(['install-hooks'])


def test_dead_fixtures():
    repo = mock()
    when(repo).ensure()
    when(epab.utils).Repo(...).thenReturn(repo)
    when(_dead_fixtures)._pytest_dead_fixtures(...)
    _check_runner_result(['pytest-dead-fixtures'])


def test_setup_config():
    with pytest.raises(FileNotFoundError):
        config.setup_config('0.0.1')
