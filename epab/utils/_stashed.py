# coding=utf-8
"""
Simple decorator to stash changed files between a destructive repo operation
"""

import functools

from epab.core import CTX


def stashed(func):
    """
    Simple decorator to stash changed files between a destructive repo operation
    """

    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        if CTX.stash and not CTX.repo.stashed:
            CTX.repo.stash(func.__name__)
            try:
                func(*args, **kwargs)
            finally:
                CTX.repo.unstash()
        else:
            func(*args, **kwargs)

    return _wrapper
