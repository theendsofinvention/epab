# coding=utf-8
"""
Manages runners
"""
import sys
import typing

import sarge

import epab.exc
import epab.utils
from epab.core import config

_DEFAULT_PROCESS_TIMEOUT = 60


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


def check_error(return_code: int, mute: bool, exe_short: str, failure_ok: bool, output: typing.List[str]) -> int:
    """
    Runs after a sub-process exits

    Checks the return code; if it is different than 0, then a few things happen:

        - if the process was muted ("mute" is True), the process output is printed anyway
        - if "failure_ok" is True (default), then a SystemExist exception is raised

    :param return_code: sub-process return code
    :param mute: mute the sub-process output
    :param exe_short: short name of the sub-process
    :param failure_ok: ignore failure
    :param output: output of the sub-process
    """
    if return_code:
        if mute:
            epab.utils.cmd_end('')
            process_output_as_str = '\n'.join(output)
            epab.utils.std_err(f'{exe_short} error:\n{process_output_as_str}')
        epab.utils.error(f'command failed: {exe_short} -> {return_code}')
        if not failure_ok:
            sys.exit(return_code)
    else:
        if mute:
            epab.utils.cmd_end(f' -> {return_code}')
        else:
            epab.utils.info(f'{exe_short} -> {return_code}')

    return return_code


def _parse_output_line(line: bytes, filters: typing.Optional[typing.Iterable[str]]):
    line_str: str = line.decode('cp437')
    filtered_line: typing.Optional[str] = filter_line(line_str, filters)
    if filtered_line:
        return filtered_line.rstrip()

    return None


def capture_output_from_running_process(
        output_so_far: typing.List[str],
        capture: sarge.Capture,
        filters: typing.Optional[typing.Iterable[str]],
        mute: bool
):
    """
    Parses output from a running sub-process

    :param output_so_far: output gathered so far (the list will be updated in-place)
    :param capture: sarge.Capture instance the output will be read from
    :param filters: filter strings
    :param mute: mute output
    """
    _output = capture.readline(block=False)
    if _output:
        line = _parse_output_line(_output, filters)
        if line:
            if not mute:
                epab.utils.std_out(line)
            output_so_far.append(line)
        return capture_output_from_running_process(output_so_far, capture, filters, mute)

    return None


def run(
        cmd: str,
        *paths: str,
        cwd: str = '.',
        mute: bool = False,
        filters: typing.Optional[typing.Iterable[str]] = None,
        failure_ok: bool = False,
        timeout: float = _DEFAULT_PROCESS_TIMEOUT,
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
        timeout: sub-process timeout

    Returns: command output
    """

    if filters and isinstance(filters, str):
        filters = [filters]

    exe = epab.utils.find_executable(cmd.split(' ')[0], *paths)
    if not exe:
        raise epab.exc.ExecutableNotFoundError(cmd.split(' ')[0])
    exe_short = exe.name

    cmd = ' '.join([f'"{exe.absolute()}"'] + cmd.split(' ')[1:])

    mute = mute and not config.VERBOSE()
    if mute:
        epab.utils.cmd_start(f'RUNNING: {cmd}')
    else:
        epab.utils.info(f'RUNNING: {cmd}')
    capture = sarge.Capture()
    process = sarge.Command(cmd, stdout=capture, stderr=capture, shell=True, cwd=cwd)
    process.run(async_=True)

    output: typing.List[str] = []
    import time
    start_time = time.monotonic()
    while True:
        capture_output_from_running_process(
            output_so_far=output,
            capture=capture,
            filters=filters,
            mute=mute,
        )
        if process.poll() is not None:
            break
        if time.monotonic() - start_time > timeout:
            epab.utils.error(f'process timeout: {exe_short} ({timeout} seconds')
            sys.exit(1)
    check_error(process.returncode, mute, exe_short, failure_ok, output)
    return '\n'.join(output), process.returncode
