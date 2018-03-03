# coding=utf-8

import string

import delegator
import pexpect
import pytest
from hypothesis import given
from hypothesis import strategies as st
from mockito import mock, unstub, verify, when

import epab.exc
import epab.utils
import epab.utils._run
from epab.utils._run import filter_line


@pytest.fixture(name='process', autouse=True)
def _process():
    process = mock()
    subprocess = mock()
    process.out = 'output'
    process.err = ''
    process.name = 'test.exe'
    process.return_code = 0
    process.subprocess = subprocess
    when(delegator).run(...).thenReturn(process)
    when(epab.utils).find_executable('test').thenReturn(process)
    when(epab.utils).cmd_start(...)
    when(epab.utils).cmd_end(...)
    when(epab.utils).info(...)
    when(epab.utils).error(...)
    when(epab.utils).std_out(...)
    when(epab.utils).std_err(...)
    yield process


@given(text=st.text(alphabet=string.printable))
def test_filter_line_raw(text):
    assert filter_line(text, None) == text


def test_filter_line():
    text = 'some random text'
    assert filter_line(text, None) == text
    assert filter_line(text, ['some']) is None
    assert filter_line(text, [' some']) == text
    assert filter_line(text, ['some ']) is None
    assert filter_line(text, ['random']) is None
    assert filter_line(text, [' random']) is None
    assert filter_line(text, ['random ']) is None
    assert filter_line(text, [' random ']) is None
    assert filter_line(text, ['text']) is None
    assert filter_line(text, [' text']) is None
    assert filter_line(text, [' text ']) == text


def test_exe_not_found():
    when(epab.utils).find_executable(...).thenReturn(None)
    with pytest.raises(epab.exc.ExecutableNotFoundError):
        epab.utils.run('test')


@pytest.mark.parametrize(
    'input_,output',
    [
        ('test', 'test'),
        ('test\n', 'test'),
        ('test\n\n', 'test'),
        ('test\n\ntest', 'test\ntest'),
        ('test\n\ntest\n', 'test\ntest'),
        ('test\n\ntest\n\n', 'test\ntest'),
    ]
)
def test_output(process, input_, output):
    process.out = input_
    out, code = epab.utils.run('test')
    verify(epab.utils).info('test.exe -> 0')
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils).std_out(output)
    verify(epab.utils, times=0).error(...)
    assert code == 0
    assert out == output


def test_mute_output():
    out, code = epab.utils.run('test', mute=True)
    verify(epab.utils, times=0).info(...)
    verify(epab.utils, times=0).error(...)
    verify(epab.utils).cmd_end(' -> 0')
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    assert code == 0
    assert out == 'output'


def test_filter_as_str(process):
    process.out = 'output\ntest'
    out, code = epab.utils.run('test', mute=True, filters='test')
    verify(epab.utils, times=0).info(...)
    verify(epab.utils, times=0).error(...)
    verify(epab.utils).cmd_end(' -> 0')
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    assert code == 0
    assert out == 'output'


def test_no_output(process):
    process.out = ''
    out, code = epab.utils.run('test')
    verify(epab.utils).info('test.exe -> 0')
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils).std_out('')
    verify(epab.utils, times=0).error(...)
    assert code == 0
    assert out == ''


def test_filtered_output():
    out, code = epab.utils.run('test', filters=['output'])
    verify(epab.utils).info('test.exe -> 0')
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils).std_out('')
    verify(epab.utils, times=0).error(...)
    assert code == 0
    assert out == ''


def test_error(process):
    process.return_code = 1
    process.out = 'some error'
    out, code = epab.utils.run('test', filters=['output'], failure_ok=True)
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils).std_err('test.exe error:\nsome error')
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils, times=1).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == 'some error'


def test_error_no_result(process):
    process.return_code = 1
    process.out = ''
    out, code = epab.utils.run('test', filters=['output'], failure_ok=True)
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == ''


def test_error_muted(process):
    process.return_code = 1
    unstub(process.subprocess)
    when(process.subprocess).read_nonblocking(1, None).thenReturn('some output').thenRaise(pexpect.exceptions.EOF(None))
    out, code = epab.utils.run('test', filters=['output'], failure_ok=True, mute=True)
    verify(epab.utils, times=0).info(...)
    verify(epab.utils).cmd_end('')
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == ''


def test_failure(process):
    process.return_code = 1
    process.out = 'error'
    with pytest.raises(SystemExit):
        epab.utils.run('test', filters=['output'])
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils).std_err('test.exe error:\nerror')
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils).error('command failed: test.exe -> 1')
