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
from ._next_version import get_next_version
from ._stashed import stashed
from ._resource_path import resource_path
from ._av import AV
from ._exe_version import get_product_version, VersionInfo
