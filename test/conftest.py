# coding=utf-8

import pytest


def pytest_addoption(parser):
    parser.addoption("--long", action="store_true",
                     help="run long tests")


def pytest_runtest_setup(item):
    longmarker = item.get_marker("long")
    if longmarker is not None and not item.config.getoption('long'):
        pytest.skip('skipping long tests')
