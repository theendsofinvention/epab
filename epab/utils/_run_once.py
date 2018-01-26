# coding=utf-8
"""
Simple decorator to ensure a function is ran only once
"""

import epab.utils
from epab.core import CTX


def run_once(func):
    """
    Simple decorator to ensure a function is ran only once
    """

    def _inner(*args, **kwargs):
        if func.__name__ in CTX.run_once:
            epab.utils.info(f'RUN_ONCE: skipping {func.__name__}')
            return CTX.run_once[func.__name__]

        epab.utils.info(f'RUN_ONCE: running {func.__name__}')
        result = func(*args, **kwargs)
        CTX.run_once[func.__name__] = result
        return result

    return _inner
