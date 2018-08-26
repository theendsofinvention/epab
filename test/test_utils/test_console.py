# coding=utf-8
"""
Pass
"""

import string

import pytest
from hypothesis import given, strategies as st

import epab.utils
from epab.core import config
# noinspection PyProtectedMember
from epab.utils._console import _sanitize


@pytest.mark.long
@given(text=st.text())
def test_sanitize(text):
    result = _sanitize(text)
    assert isinstance(result, str)
    result.encode('ascii')


@pytest.mark.long
@given(text=st.text(alphabet=string.printable))
def test_info(text, capsys):
    epab.utils.info(text)
    out, err = capsys.readouterr()
    assert out == 'EPAB: {}\n'.format(text)
    assert err == ''


@pytest.mark.long
@given(text=st.text(alphabet=string.printable))
def test_cmd_end(text, capsys):
    epab.utils.cmd_end(text)
    out, err = capsys.readouterr()
    assert out == '{}\n'.format(text)
    assert err == ''


@pytest.mark.parametrize(
    'func,out,err',
    [
        (epab.utils.info, 'EPAB: {}\n', ''),
        (epab.utils.error, '', 'EPAB: {}\n'),
        (epab.utils.cmd_start, 'EPAB: {}', ''),
        (epab.utils.cmd_end, '{}\n', ''),
        (epab.utils.std_err, '', '{}\n'),
        (epab.utils.std_out, '{}\n', ''),
    ],
    ids=['info', 'error', 'cmd_start', 'cmd_end', 'std_err', 'std_out']
)
@given(text=st.text(alphabet=string.printable))
def test_not_quiet(func, out, err, text, capsys):
    func(text)
    _out, _err = capsys.readouterr()
    assert out.format(text) == _out
    assert err.format(text) == _err


@pytest.mark.parametrize(
    'func',
    [
        epab.utils.info,
        epab.utils.error,
        epab.utils.cmd_start,
        epab.utils.cmd_end,
        epab.utils.std_err,
        epab.utils.std_out,
    ],
    ids=['info', 'error', 'cmd_start', 'cmd_end', 'std_err', 'std_out']
)
@given(text=st.text(alphabet=string.printable))
def test_quiet(func, text, capsys):
    config.QUIET.default = True
    func(text)
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''
