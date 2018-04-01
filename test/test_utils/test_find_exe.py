# coding=utf-8

import sys
from pathlib import Path

import epab.utils
from epab.core import CTX


def test_find_executable():
    python = epab.utils.find_executable('python')
    assert epab.utils.find_executable('python.exe') == python
    assert epab.utils.find_executable('python', f'{sys.prefix}/Scripts') == python
    assert epab.utils.find_executable('__sure__not__') is None


def test_context():
    assert epab.utils.find_executable('__sure__not__') is None
    CTX.known_executables['__sure__not__.exe'] = 'ok'
    assert epab.utils.find_executable('__sure__not__') == 'ok'


def test_paths():
    assert epab.utils.find_executable('python')
    assert epab.utils.find_executable('python', '.')
    CTX.known_executables = {}
    assert epab.utils.find_executable('python', '.') is None


def test_direct_find():
    exe = Path('test.exe')
    exe.touch()
    assert exe.absolute() == epab.utils.find_executable('test')
