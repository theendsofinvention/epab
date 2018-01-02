# coding=utf-8
"""
Contains various utility functions
"""
from ._console import error, info, cmd_start, std_out, cmd_end
from ._do import do, do_ex, find_executable
from ._repo import repo_ensure, repo_get_latest_tag, repo_get_current_branch, repo_is_dirty, repo_commit,\
    repo_checkout, repo_merge, repo_push, repo_tag, repo_remove_tag, repo_is_on_tag
from ._run_once import run_once
from ._temp_dir import temporary_working_dir
from ._version import bump_version
from ._dry_run import dry_run


def ensure_exe(exe_name: str, path: str = None):
    """
    Makes sure that an executable can be found on the system path.
    Will exit the program if the executable cannot be found

    Args:
        exe_name: name of the executable
        path: optional path to be searched; if not specified, search the whole system

    """
    if not find_executable(exe_name, path):
        error(f'Could not find "{exe_name}.exe" on this system')
        exit(-1)
