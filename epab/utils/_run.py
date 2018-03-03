# coding=utf-8
"""
Manages runners
"""
import sys
import typing

import delegator

import epab.exc
import epab.utils
from epab.core import CONFIG


def filter_line(
        line: str,
        filters: typing.Optional[typing.Iterable[str]]
) -> typing.Optional[str]:
    """
    Filters out line that contain substring

    Args:
        line: line to filter
        filters: filter strings to apply

    Returns: line if not filter are found in line, else None

    """
    if filters is not None:
        for filter_ in filters:
            if filter_ in line:
                return None
    return line


def _parse_output(process, filters):
    result = []
    for line in process.out.splitlines():
        if filter_line(line, filters):
            result.append(line)
    for line in process.err.splitlines():  # pragma: no cover
        if filter_line(line, filters):
            result.append(line)

    return '\n'.join(result)


def _process_run_result(process, mute, exe_short, failure_ok, result) -> typing.Tuple[str, int]:
    if process.return_code:
        if mute:
            epab.utils.cmd_end('')
        epab.utils.error(f'command failed: {exe_short} -> {process.return_code}')
        if result:
            epab.utils.std_err(f'{exe_short} error:\n{result}')
            if not result.endswith('\n'):  # pragma: no cover
                print()
        if not failure_ok:
            sys.exit(process.return_code)
    else:
        if mute:
            epab.utils.cmd_end(f' -> {process.return_code}')
        else:
            epab.utils.std_out(result)
            if not result.endswith('\n'):  # pragma: no cover
                print()
            epab.utils.info(f'{exe_short} -> {process.return_code}')

    return result, process.return_code


def run(
        cmd: str,
        *paths: str,
        cwd: str = '.',
        mute: bool = False,
        filters: typing.Union[None, typing.Iterable[str]] = None,
        failure_ok: bool = False,
) -> typing.Tuple[str, int]:
    """
    Executes a command and returns the result

    Args:
        cmd: command to execute
        paths: paths to search executable in
        cwd: working directory (defaults to ".")
        mute: if true, output will not be printed
        filters: gives a list of partial strings to filter out from the output (stdout or stderr)
        failure_ok: if False (default), a return code different than 0 will exit the application

    Returns: command output
    """

    if filters and isinstance(filters, str):
        filters = [filters]

    exe = epab.utils.find_executable(cmd.split(' ')[0], *paths)
    if not exe:
        raise epab.exc.ExecutableNotFoundError(cmd.split(' ')[0])
    exe_short = exe.name

    cmd = ' '.join([f'"{exe.absolute()}"'] + cmd.split(' ')[1:])

    mute = mute and not CONFIG.verbose

    if mute:
        epab.utils.cmd_start(f'RUNNING: {cmd}')
    else:
        epab.utils.info(f'RUNNING: {cmd}')

    process = delegator.run(cmd, block=True, cwd=cwd, binary=False)
    result = _parse_output(process, filters)

    return _process_run_result(process, mute, exe_short, failure_ok, result)
