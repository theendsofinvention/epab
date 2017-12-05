# coding=utf-8
import os

import click

from ._console import _error, _info
from ._do import do, do_ex
from ._dry_run import dry_run


def repo_get_current_branch(ctx) -> str:
    return do(ctx, 'git rev-parse --abbrev-ref HEAD', mute_stdout=True)


def repo_tag(ctx: click.Context, tag: str):
    _info(f'Tagging repo: {tag}')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'tag', tag])


def repo_remove_tag(ctx: click.Context, tag: str):
    _info(f'Removing tag: {tag}')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'tag', '-d', tag])


def repo_get_latest_tag(ctx) -> str:
    return do(ctx, 'git describe --dirty --tags --long', mute_stdout=True)


def repo_ensure(ctx):
    """
    Makes sure the current working directory is a Git repository.
    """
    _info('checking repository')
    if not os.path.exists('.git') or not os.path.exists(ctx.obj['CONFIG']['package']):
        _error('This command is meant to be ran in a Git repository.\n'
               'You can clone the repository by running:\n\n'
               f'\tgit clone https://github.com/132nd-etcher/{ctx.obj["CONFIG"]["package"]}.git\n\n'
               'Then cd into it and try again.', )
        if dry_run(ctx):
            return
        exit(-1)


def repo_commit(ctx: click.Context, message: str, extended: str = None):
    if extended:
        message = f'{message}\n\n{extended}'
    _info(f'Committing all changes with message: {message}')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'add', '.'])
    out, err, code = do_ex(ctx, ['git', 'commit', '-m', message])
    if code:
        if err:
            _error(err)
        if 'nothing to commit, working tree clean' in out:
            _info('Nothing to commit, working tree clean')
            return
        else:
            _error(out)
            exit(code)


def repo_checkout(ctx: click.Context, ref_name: str):
    if repo_is_dirty(ctx):
        _error(f'Repository is dirty; cannot checkout "{ref_name}"')
        exit(-1)
    _info(f'Checking out {ref_name}')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'checkout', ref_name])


def repo_merge(ctx: click.Context, ref_name: str):
    if repo_is_dirty(ctx):
        _error(f'Repository is dirty; cannot merge "{ref_name}"')
        exit(-1)
    current_branch = repo_get_current_branch(ctx)
    _info(f'Merging {ref_name} into {current_branch}')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'merge', ref_name])


def repo_push(ctx: click.Context):
    _info('Pushing repo to origin')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'push'])


def repo_is_dirty(ctx: click.Context) -> bool:
    """
    Checks if the current repository contains uncommitted or untracked changes

    Returns: true if the repository is clean
    """
    out, _, _ = do_ex(ctx, ['git', 'status', '--porcelain', '--untracked-files=no'])
    result = bool(out)
    if dry_run(ctx) and result:
        _info('Repo was dirty; DRYRUN')
        return False
    return result
