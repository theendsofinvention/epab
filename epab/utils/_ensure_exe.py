# coding=utf-8
"""
Makes sure that an executable can be found on the system path.
Will exit the program if the executable cannot be found
"""
import logging
import sys

import elib_run

LOGGER = logging.getLogger('EPAB')


def ensure_exe(exe_name: str, *paths: str):  # pragma: no cover
    """
    Makes sure that an executable can be found on the system path.
    Will exit the program if the executable cannot be found

    Args:
        exe_name: name of the executable
        paths: optional path(s) to be searched; if not specified, search the whole system

    """
    if not elib_run.find_executable(exe_name, *paths):
        LOGGER.error('could not find "%s.exe" on this system', exe_name)
        sys.exit(-1)
