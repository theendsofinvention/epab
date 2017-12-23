# coding=utf-8
"""
Runs external applications
"""
import os
import shlex
import subprocess
import sys
import typing

import click
from epab.utils import _cmd, _cmd_out, _error, _out


def find_executable(executable: str, path: str = None) -> typing.Union[str, None]:  # noqa: C901
    # noinspection SpellCheckingInspection
    """
    https://gist.github.com/4368898

    Public domain code by anatoly techtonik <techtonik@gmail.com>

    Programmatic equivalent to Linux `which` and Windows `where`

    Find if ´executable´ can be run. Looks for it in 'path'
    (string that lists directories separated by 'os.pathsep';
    defaults to os.environ['PATH']). Checks for all executable
    extensions. Returns full path or None if no command is found.

    Args:
        executable: executable name to look for
        path: root path to examine (defaults to system PATH)

    Returns: executable path as string or None

    """

    if not executable.endswith('.exe'):
        executable = f'{executable}.exe'

    if executable in find_executable.known_executables:  # type: ignore
        return find_executable.known_executables[executable]  # type: ignore

    _cmd(f'Looking for executable: {executable}')

    if path is None:
        path = os.environ['PATH']
    paths = [os.path.abspath(os.path.join(
        sys.exec_prefix, 'Scripts'))] + path.split(os.pathsep)
    if os.path.isfile(executable):
        executable_path = os.path.abspath(executable)
    else:
        for path_ in paths:
            executable_path = os.path.join(path_, executable)
            if os.path.isfile(executable_path):
                break
        else:
            _cmd_out(f' -> not found')
            return None

    # type: ignore
    find_executable.known_executables[executable] = executable_path
    _cmd_out(f' -> {click.format_filename(executable_path)}')
    return executable_path


find_executable.known_executables = {}  # type: ignore


def do_ex(ctx: click.Context, cmd: typing.List[str], cwd: str = '.') -> typing.Tuple[str, str, int]:
    """
    Executes a given command

    Args:
        ctx: Click context
        cmd: command to run
        cwd: working directory (defaults to ".")

    Returns: stdout, stderr, exit_code

    """

    def _popen_pipes(cmd_, cwd_):
        def _always_strings(env_dict):
            """
            On Windows and Python 2, environment dictionaries must be strings
            and not unicode.
            """
            env_dict.update(
                (key, str(value))
                for (key, value) in env_dict.items()
            )
            return env_dict

        return subprocess.Popen(
            cmd_,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(cwd_),
            env=_always_strings(
                dict(
                    os.environ,
                    # try to disable i18n
                    LC_ALL='C',
                    LANGUAGE='',
                    HGPLAIN='1',
                )
            )
        )

    def _ensure_stripped_str(_, str_or_bytes):
        if isinstance(str_or_bytes, str):
            return '\n'.join(str_or_bytes.strip().splitlines())

        return '\n'.join(str_or_bytes.decode('utf-8', 'replace').strip().splitlines())

    exe = find_executable(cmd.pop(0))
    if not exe:
        exit(-1)
    cmd.insert(0, exe)
    _cmd(f'{cmd}')
    process = _popen_pipes(cmd, cwd)
    out, err = process.communicate()
    _cmd_out(f' -> {process.returncode}')
    return _ensure_stripped_str(ctx, out), _ensure_stripped_str(ctx, err), process.returncode


def do(  # pylint: disable=too-many-arguments,invalid-name
        ctx,
        cmd,
        cwd: str = '.',
        mute_stdout: bool = False,
        mute_stderr: bool = False,
        # @formatter:off
        filter_output: typing.Union[None, typing.Iterable[str]] = None
        # @formatter:on
) -> str:
    """
    Executes a command and returns the result

    Args:
        ctx: click context
        cmd: command to execute
        cwd: working directory (defaults to ".")
        mute_stdout: if true, stdout will not be printed
        mute_stderr: if true, stderr will not be printed
        filter_output: gives a list of partial strings to filter out from the output (stdout or stderr)

    Returns: stdout
    """

    def _filter_output(input_):

        def _filter_line(line):
            # noinspection PyTypeChecker
            for filter_str in filter_output:
                if filter_str in line:
                    return False
            return True

        if filter_output is None:
            return input_
        return '\n'.join(filter(_filter_line, input_.split('\n')))

    if not isinstance(cmd, (list, tuple)):
        cmd = shlex.split(cmd)

    out, err, ret = do_ex(ctx, cmd, cwd)
    if out and not mute_stdout:
        _out(f'{_filter_output(out)}')
    if err and not mute_stderr:
        _cmd(f'{_filter_output(err)}')
    if ret:
        _error(f'command failed: {cmd}')
        exit(ret)
    return out
