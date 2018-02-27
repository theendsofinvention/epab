# coding=utf-8
"""
Pass
"""

import string

import pytest
from hypothesis import given
from hypothesis import strategies as st

import epab.utils
from epab.core import CONFIG
# noinspection PyProtectedMember
from epab.utils._console import _sanitize


@given(text=st.text())
def test_sanitize(text):
    result = _sanitize(text)
    assert isinstance(result, str)
    result.encode('ascii')


@given(text=st.text(alphabet=string.printable))
def test_info(text, capsys):
    epab.utils.info(text)
    out, err = capsys.readouterr()
    assert out == 'EPAB: {}\n'.format(text)
    assert err == ''


@given(text=st.text(alphabet=string.printable))
def test_cmd_end(text, capsys):
    epab.utils.cmd_end(text)
    out, err = capsys.readouterr()
    assert out == '{}\n'.format(text)
    assert err == ''


# @given(text=st.text(alphabet=string.printable))
# def test_cmd_start(text, capsys):
#     epab.utils.cmd_start(text)
#     out, err = capsys.readouterr()
#     assert out == 'EPAB: {}'.format(text)
#     assert err == ''


# @given(text=st.text(alphabet=string.printable))
# def test_std_err(text, capsys):
#     epab.utils.std_err(text)
#     out, err = capsys.readouterr()
#     assert out == ''
#     assert err == 'EPAB: {}\n'.format(text)


# @given(text=st.text(alphabet=string.printable))
# def test_std_out(text, capsys):
#     epab.utils.std_out(text)
#     out, err = capsys.readouterr()
#     assert out == text
#     assert err == ''


# @given(text=st.text(alphabet=string.printable))
# def test_error(text, capsys):
#     epab.utils.error(text)
#     out, err = capsys.readouterr()
#     assert out == ''
#     assert err == 'EPAB: {}\n'.format(text)


@pytest.mark.parametrize(
    'func,out,err',
    [
        (epab.utils.info, 'EPAB: {}\n', ''),
        (epab.utils.error, '', 'EPAB: {}\n'),
        (epab.utils.cmd_start, 'EPAB: {}', ''),
        (epab.utils.cmd_end, '{}\n', ''),
        (epab.utils.std_err, '', '{}\n'),
        (epab.utils.std_out, '{}', ''),
    ],
    ids=['info', 'error', 'cmd_start', 'cmd_end', 'std_err', 'std_out']
)
@given(text=st.text(alphabet=string.printable))
def test_quiet(func, out, err, text, capsys):
    CONFIG.quiet = False
    func(text)
    _out, _err = capsys.readouterr()
    assert _out == out.format(text)
    assert _err == err.format(text)
    CONFIG.quiet = True
    func(text)
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''
