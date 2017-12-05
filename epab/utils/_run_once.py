# coding=utf-8

from ._console import _info


def run_once(func):
    def inner(ctx, *args, **kwargs):
        if func.__name__ in ctx.obj['run_once']:
            _info(f'RUN_ONCE: skipping {func.__name__}')
            return

        _info(f'RUN_ONCE: running {func.__name__}')
        ctx.obj['run_once'].append(func.__name__)
        return func(ctx, *args, **kwargs)

    return inner
