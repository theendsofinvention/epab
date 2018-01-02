# coding=utf-8
"""
Runs external applications
"""
import os
import shlex
import subprocess
import sys
import typing
from pathlib import Path

import click

from ._console import cmd_end, cmd_start, error, std_err, std_out


def find_executable(executable: str, path: str = None) -> typing.Optional[Path]:  # noqa: C901
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

    cmd_start(f'Looking for executable: {executable}')

    if path is None:
        path = os.environ['PATH']
    paths = [Path(sys.exec_prefix, 'Scripts').absolute()] + path.split(os.pathsep)
    executable_path = Path(executable)
    if not executable_path.is_file():
        for path_ in paths:
            executable_path = Path(path_, executable).absolute()
            if executable_path.is_file():
                break
        else:
            cmd_end(f' -> not found')
            return None

    find_executable.known_executables[executable] = executable_path
    cmd_end(f' -> {click.format_filename(str(executable_path))}')
    return executable_path


find_executable.known_executables = {}


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

    cmd_start(f'{cmd}')
    process = _popen_pipes(cmd, cwd)
    out, err = process.communicate()
    cmd_end(f' -> {process.returncode}')
    return _ensure_stripped_str(ctx, out), _ensure_stripped_str(ctx, err), process.returncode


def _filter_output(input_, filter_output):

    def _filter_line(line):
        # noinspection PyTypeChecker
        for filter_str in filter_output:
            if filter_str in line:
                return False
        return True

    if filter_output is None:
        return input_
    return '\n'.join(filter(_filter_line, input_.split('\n')))


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

    if not isinstance(cmd, (list, tuple)):
        cmd = shlex.split(cmd)

    exe = find_executable(cmd.pop(0))
    if not exe:
        exit(-1)
    cmd.insert(0, str(exe.absolute()))

    out, err, ret = do_ex(ctx, cmd, cwd)
    if out and not mute_stdout:
        std_out(exe.name, f'{_filter_output(out, filter_output)}')
    if err and not mute_stderr:
        std_err(exe.name, f'{_filter_output(err, filter_output)}')
    if ret:
        error(f'command failed: {cmd}')
        exit(ret)
    return out
