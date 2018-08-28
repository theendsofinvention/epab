# coding=utf-8

import os
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner
from mockito import unstub

from epab.core import CTX, config


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
    CTX._reset()
    config.CHANGELOG_DISABLE.default = False
    config.ARTIFACTS.default = []
    config.TEST_RUNNER_OPTIONS.default = ''
    config.TEST_AV_RUNNER_OPTIONS.default = '--long'
    config.PACKAGE_NAME.default = 'test_package'
    config.FREEZE_ENTRY_POINT.default = ''
    config.QT_RES_SRC.default = ''
    config.QT_RES_TGT.default = ''
    config.QUIET.default = False
    config.MYPY_ARGS.default = ''
    # CONFIG.load()
    current_dir = os.getcwd()
    folder = Path(tmpdir).absolute()
    os.chdir(folder)
    yield
    unstub()
    os.chdir(current_dir)


@pytest.fixture()
def dummy_git_repo():
    null = open(os.devnull, 'w')

    def create():
        subprocess.check_call(('git', 'init'), stdout=null)
        Path('./init').touch()
        subprocess.check_call(('git', 'add', './init'), stdout=null)
        subprocess.check_call(('git', 'commit', '-m', 'init commit'), stdout=null)

    dummy_git_repo.create = create

    yield dummy_git_repo


@pytest.fixture()
def cli_runner():
    yield CliRunner()
