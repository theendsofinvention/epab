# coding=utf-8
"""
Simple decorator to ensure a function is ran only once
"""

import logging

from epab.core import CTX

LOGGER = logging.getLogger('EPAB')


def run_once(func):
    """
    Simple decorator to ensure a function is ran only once
    """

    def _inner(*args, **kwargs):
        if func.__name__ in CTX.run_once:
            LOGGER.info('skipping %s', func.__name__)
            return CTX.run_once[func.__name__]

        LOGGER.info('running: %s', func.__name__)
        result = func(*args, **kwargs)
        CTX.run_once[func.__name__] = result
        return result

    return _inner
