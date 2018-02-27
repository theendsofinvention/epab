# coding=utf-8

from pathlib import Path

import pytest

import epab.utils

HERE = Path('.').absolute()


def test_exe_version():
    version = epab.utils.get_product_version(HERE.joinpath('test/test_files/version_ok.exe'))
    assert isinstance(version, epab.utils.VersionInfo)
    assert version.file_version == '0.1.0'
    assert version.full_version == 'some+very-special.version'
    assert str(version) == '0.1.0'


def test_exe_no_version():
    with pytest.raises(RuntimeError):
        epab.utils.get_product_version(HERE.joinpath('test/test_files/no_version.exe'))


def test_exe_missing_attrib():
    with pytest.raises(RuntimeError):
        epab.utils.get_product_version(HERE.joinpath('test/test_files/missing_attrib.exe'))
