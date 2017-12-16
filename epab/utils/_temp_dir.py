# coding=utf-8
"""
Context to temporarily change the working directory
"""


import os
from contextlib import contextmanager


@contextmanager
def temporary_working_dir(path):
    """
    Context to temporarily change the working directory

    Args:
        path: working directory to cd into
    """
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)
