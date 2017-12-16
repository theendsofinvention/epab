# coding=utf-8

from ._console import _info


def run_once(func):
    def inner(ctx, *args, **kwargs):
        if func.__name__ in ctx.obj['run_once']:
            _info(f'RUN_ONCE: skipping {func.__name__}')
            return ctx.obj['run_once'][func.__name__]

        _info(f'RUN_ONCE: running {func.__name__}')
        result = func(ctx, *args, **kwargs)
        ctx.obj['run_once'][func.__name__] = result
        return result

    return inner
