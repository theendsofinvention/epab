# coding=utf-8

import os
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner
from mockito import unstub, verifyNoUnwantedInteractions, verifyStubbedInvocationsAreUsed

# noinspection PyProtectedMember
from epab._logging import _setup_logging
from epab.core import CTX, config as epab_config


def pytest_configure(config):
    """
    Runs at tests startup

    Args:
        config: pytest config args
    """
    print('Pytest config:', config.option)
    setattr(sys, '_called_from_test', True)


# noinspection SpellCheckingInspection
def pytest_unconfigure(config):
    """Tear down"""
    assert config
    delattr(sys, '_called_from_test')


def pytest_addoption(parser):
    parser.addoption("--long", action="store_true",
                     help="run long tests")


def pytest_runtest_setup(item):
    long_marker = item.get_marker("long")
    if long_marker is not None and not item.config.getoption('long'):
        pytest.skip(f'{item.location}: skipping long tests')


@pytest.fixture(autouse=True)
def _global_tear_down(tmpdir, monkeypatch):
    """
    Maintains a sane environment between tests
    """
    try:
        monkeypatch.delenv('APPVEYOR')
    except KeyError:
        pass
    # noinspection PyProtectedMember
    CTX._reset()
    orig_dir = os.getcwd()
    epab_config.CHANGELOG_DISABLE.default = False
    epab_config.ARTIFACTS.default = []
    epab_config.TEST_RUNNER_OPTIONS.default = ''
    epab_config.TEST_AV_RUNNER_OPTIONS.default = '--long'
    epab_config.PACKAGE_NAME.default = 'test_package'
    epab_config.FREEZE_ENTRY_POINT.default = ''
    epab_config.QT_RES_SRC.default = ''
    epab_config.QT_RES_TGT.default = ''
    epab_config.QUIET.default = False
    epab_config.MYPY_ARGS.default = ''
    folder = Path(tmpdir).absolute()
    os.chdir(folder)
    yield
    os.chdir(orig_dir)


@pytest.fixture(autouse=True, scope='session')
def _logging():
    _setup_logging()


@pytest.fixture(autouse=True)
def _mockito():
    unstub()
    yield
    verifyNoUnwantedInteractions()
    verifyStubbedInvocationsAreUsed()
    unstub()


@pytest.fixture(autouse=True)
def _clean_os_env():
    env = os.environ.copy()
    yield
    for key, value in env.items():
        os.environ[key] = value
    for key in os.environ.keys():
        if key not in env.keys():
            del os.environ[key]


@pytest.fixture()
def dummy_git_repo():
    """
    Creates a dummy Git repo in the current directory
    """
    null = open(os.devnull, 'w')

    def _create():
        subprocess.check_call(('git', 'init'), stdout=null)
        Path('./init').touch()
        subprocess.check_call(('git', 'add', './init'), stdout=null)
        subprocess.check_call(('git', 'commit', '-m', 'init commit'), stdout=null)

    dummy_git_repo.create = _create

    yield dummy_git_repo


@pytest.fixture()
def cli_runner():
    """
    Click CLI runner for tests
    """
    yield CliRunner()
