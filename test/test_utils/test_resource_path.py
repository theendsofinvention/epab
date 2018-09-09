# coding=utf-8
import sys
from pathlib import Path

import pytest
from mockito import verifyStubbedInvocationsAreUsed, when

import epab.utils._resource_path

HERE = Path('.').absolute()


def test_from_dev():
    assert epab.utils.resource_path(HERE.joinpath('epab'), '__main__.py').exists()


def test_from_sys():
    setattr(sys, '_MEIPASS', str(HERE))
    assert epab.utils.resource_path('epab', 'epab/__main__.py').exists()


def test_from_package():
    when(epab.utils._resource_path)._get_from_package(
        'epab', Path('__main__.py')
    ).thenReturn(
        Path(HERE, 'epab/__main__.py')
    )
    assert epab.utils.resource_path('epab', '__main__.py').exists()
    verifyStubbedInvocationsAreUsed()


def test_not_found():
    with pytest.raises(FileNotFoundError):
        epab.utils.resource_path('epab', 'nope')
