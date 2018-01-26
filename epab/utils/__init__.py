# coding=utf-8
"""
Contains various utility functions
"""
from ._console import error, info, cmd_start, std_out, cmd_end, std_err
from ._run import run
from ._ensure_exe import ensure_exe
from ._find_exe import find_executable
from ._repo import Repo
from ._run_once import run_once
from ._gitversion import get_git_version_info
from ._stashed import stashed
