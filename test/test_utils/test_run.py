# coding=utf-8

import string

import pytest
import sarge
from hypothesis import given, strategies as st
from mockito import mock, verify, when

import epab.exc
import epab.utils
# noinspection PyProtectedMember
from epab.utils._run import filter_line

_RUN_FUNC = epab.utils.run


@pytest.fixture(name='sarge_proc')
def _command():
    exe = mock()
    exe.name = 'test.exe'
    command = mock()
    command.returncode = 0
    capture = mock()
    when(epab.utils).find_executable('test').thenReturn(exe)
    when(epab.utils).cmd_start(...)
    when(epab.utils).cmd_end(...)
    when(epab.utils).info(...)
    when(epab.utils).error(...)
    when(epab.utils).std_out(...)
    when(epab.utils).std_err(...)
    when(sarge).Command(...).thenReturn(command)
    when(sarge).Capture().thenReturn(capture)
    when(command).run(...)
    yield command, capture


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
        _RUN_FUNC('test')


def test_basic(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'test output').thenReturn(None)
    output, returncode = _RUN_FUNC('test')
    assert returncode is 0
    assert 'test output' == output


@pytest.mark.parametrize(
    'input_,output',
    [
        (b'test', 'test'),
        (b'test\n', 'test'),
        (b'test\n\n', 'test'),
        (b'test\n\ntest', 'test\n\ntest'),
        (b'test\n\ntest\n', 'test\n\ntest'),
        (b'test\n\ntest\n\n', 'test\n\ntest'),
    ]
)
def test_output(sarge_proc, input_, output):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(input_).thenReturn(None)
    # process.out = input_
    out, code = _RUN_FUNC('test')
    verify(epab.utils).info('test.exe -> 0')
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils).std_out(output)
    verify(epab.utils, times=0).error(...)
    assert code == 0
    assert out == output


def test_mute_output(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'output').thenReturn(None)
    out, code = _RUN_FUNC('test', mute=True)
    verify(epab.utils, times=0).info(...)
    verify(epab.utils, times=0).error(...)
    verify(epab.utils).cmd_end(' -> 0')
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    assert code == 0
    assert out == 'output'


def test_multi_line_output(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'output').thenReturn(b'test').thenReturn(None)
    out, code = _RUN_FUNC('test', mute=True)
    verify(epab.utils, times=0).info(...)
    verify(epab.utils, times=0).error(...)
    verify(epab.utils).cmd_end(' -> 0')
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    assert code == 0
    assert 'output\ntest' == out


def test_filter_as_str(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'output').thenReturn(b'test').thenReturn(None)
    out, code = _RUN_FUNC('test', mute=True, filters='test')
    verify(epab.utils, times=0).info(...)
    verify(epab.utils, times=0).error(...)
    verify(epab.utils).cmd_end(' -> 0')
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    assert code == 0
    assert 'output' == out


def test_filter_as_list(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'output').thenReturn(b'test').thenReturn(None)
    out, code = _RUN_FUNC('test', filters=['output', 'test'])
    verify(epab.utils).info('test.exe -> 0')
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils, times=0).error(...)
    assert code == 0
    assert '' == out


def test_no_output(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(None)
    out, code = _RUN_FUNC('test')
    verify(epab.utils).info('test.exe -> 0')
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils, times=0).error(...)
    assert code == 0
    assert out == ''


def test_error(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'some error').thenReturn(None)
    out, code = _RUN_FUNC('test', failure_ok=True, filters=['test'])
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils).std_out('some error')
    verify(epab.utils).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == 'some error'


def test_error_muted_process(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'some error').thenReturn(None)
    out, code = _RUN_FUNC('test', failure_ok=True, filters=['test'], mute=True)
    verify(epab.utils).cmd_start(...)
    verify(epab.utils).cmd_end(...)
    verify(epab.utils).std_err('test.exe error:\nsome error')
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == 'some error'


def test_error_no_result(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(None)
    out, code = _RUN_FUNC('test', failure_ok=True)
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == ''


def test_error_muted(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(None)
    out, code = _RUN_FUNC('test', failure_ok=True, mute=True)
    verify(epab.utils, times=0).info(...)
    verify(epab.utils).cmd_start(...)
    verify(epab.utils).cmd_end('')
    verify(epab.utils).std_err(...)
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == ''


def test_failure(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'error').thenReturn(None)
    with pytest.raises(SystemExit):
        _RUN_FUNC('test')
    verify(epab.utils, times=0).cmd_start(...)
    verify(epab.utils, times=0).cmd_end(...)
    verify(epab.utils, times=0).std_err(...)
    verify(epab.utils).std_out('error')
    verify(epab.utils).error('command failed: test.exe -> 1')


def test_failure_muted(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'error').thenReturn(None)
    with pytest.raises(SystemExit):
        _RUN_FUNC('test', mute=True)
    verify(epab.utils).cmd_start(...)
    verify(epab.utils).cmd_end(...)
    verify(epab.utils).std_err('test.exe error:\nerror')
    verify(epab.utils, times=0).std_out(...)
    verify(epab.utils).error('command failed: test.exe -> 1')


def test_polling(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 0
    when(command).poll().thenReturn(None).thenReturn(None).thenReturn(True)
    when(capture).readline(...).thenReturn(b'out1').thenReturn(b'out2').thenReturn(b'out3').thenReturn(None)
    out, code = _RUN_FUNC('test')
    assert code is 0
    assert 'out1\nout2\nout3' == out


def test_process_timeout(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(None)
    with pytest.raises(SystemExit):
        _RUN_FUNC('test', timeout=0.1)
