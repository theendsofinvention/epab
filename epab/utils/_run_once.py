# coding=utf-8
"""
Simple decorator to ensure a function is ran only once
"""

from ._console import info


def run_once(func):
    """
    Simple decorator to ensure a function is ran only once
    """

    def _inner(ctx, *args, **kwargs):
        if func.__name__ in ctx.obj['run_once']:
            info(f'RUN_ONCE: skipping {func.__name__}')
            return ctx.obj['run_once'][func.__name__]

        info(f'RUN_ONCE: running {func.__name__}')
        result = func(ctx, *args, **kwargs)
        ctx.obj['run_once'][func.__name__] = result
        return result

    return _inner
