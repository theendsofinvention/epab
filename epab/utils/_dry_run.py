# coding=utf-8
"""
Commodity function to return dry-run state
"""


def dry_run(ctx) -> bool:
    """
    Returns: dry-run state as a bool
    """
    return ctx.obj['dry_run']
