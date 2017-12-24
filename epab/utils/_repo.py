# coding=utf-8
"""
Manages the local Git repo
"""
import os

import click

from ._console import _error, _info
from ._do import do, do_ex
from ._dry_run import dry_run


def repo_get_current_branch(ctx) -> str:
    """
    Returns: current branch as a string
    """
    return do(ctx, 'git rev-parse --abbrev-ref HEAD', mute_stdout=True)


def repo_tag(ctx: click.Context, tag: str):
    """
    Tags the repo

    Args:
        tag: tag as a string
    """
    _info(f'Tagging repo: {tag}')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'tag', tag])


def repo_remove_tag(ctx: click.Context, tag: str):
    """
    Deletes a tag from the repo

    Args:
        tag: tag to remove
    """
    _info(f'Removing tag: {tag}')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'tag', '-d', tag])


def repo_get_latest_tag(ctx) -> str:
    """
    Returns: latest tag on the repo in the form TAG+[DISTANCE+[DIRTY]]
    """
    return do(ctx, 'git describe --tags', mute_stdout=True)


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


def repo_commit(ctx: click.Context, message: str, extended: str = None, files_to_add: list = None):
    """
    Commits changes to the repo

    Args:
        message: first line of the message
        extended: optional extended message
        files_to_add: optional list of files to commit
    """
    if os.getenv('APPVEYOR_REPO_BRANCH'):
        message = f'{message} [skip ci]'
    if extended:
        message = f'{message}\n\n{extended}'
    _info(f'Committing all changes with message: {message}')
    if dry_run(ctx):
        return
    if files_to_add is None:
        do(ctx, ['git', 'add', '.'])
    else:
        _info('resetting changes')
        do(ctx, ['git', 'reset'])
        do(ctx, ['git', 'add'] + files_to_add)
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
    """
    Checks out a branch in the repo

    Args:
        ref_name: branch to check out
    """
    if repo_is_dirty(ctx):
        _error(f'Repository is dirty; cannot checkout "{ref_name}"')
        exit(-1)
    _info(f'Checking out {ref_name}')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'checkout', ref_name])


def repo_merge(ctx: click.Context, ref_name: str):
    """
    Merges two refs

    Args:
        ref_name: ref to merge in the current one
    """
    if repo_is_dirty(ctx):
        _error(f'Repository is dirty; cannot merge "{ref_name}"')
        exit(-1)
    current_branch = repo_get_current_branch(ctx)
    _info(f'Merging {ref_name} into {current_branch}')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'merge', ref_name])


def repo_push(ctx: click.Context):
    """
    Pushes all refs (branches and tags) to origin
    """
    _info('Pushing repo to origin')
    if dry_run(ctx):
        return
    do(ctx, ['git', 'push', '--all'])
    do(ctx, ['git', 'push', '--tags'])


def repo_is_dirty(ctx: click.Context) -> bool:
    """
    Checks if the current repository contains uncommitted or untracked changes

    Returns: true if the repository is clean
    """
    out, _, _ = do_ex(
        ctx, ['git', 'status', '--porcelain', '--untracked-files=no'])
    _info(out)
    result = bool(out)
    if dry_run(ctx) and result:
        _info('Repo was dirty; DRYRUN')
        return False
    return result
