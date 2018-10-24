# coding=utf-8

# coding=utf-8
"""
Collections of tools to build a python app
"""
import logging
import os
import sys

import click

import epab.cmd
import epab.linters
import epab.utils
from epab import __version__
from epab._logging import _setup_logging
from epab.core import CTX, config

config.setup_config(__version__)

LOGGER = logging.getLogger('EPAB')

_GIT_IGNORE = (
    '.idea/',
    '.cache',
    '/dist/',
    '/build/',
    '__pycache__',
    '*.spec',
    '.coverage*',
    '/.pytest_cache/',
    'htmlcov',
    'coverage.xml',
    '.hypothesis/',
    '*.egg-info/',
    '.mypy_cache',
    f'packages_{config.PACKAGE_NAME()}.png',
    f'classes_{config.PACKAGE_NAME()}.png',

)


@click.group()
@click.option('-v', '--version',
              is_flag=True, is_eager=True, expose_value=False, callback=epab.cmd.print_version, default=False,
              help='Print version and exit')
@click.option('-nv', '--next-version',
              is_flag=True, is_eager=True, expose_value=False, callback=epab.cmd.next_version, default=False,
              help='Print next version and exit')
@click.option('-d', '--dirty', is_flag=True, default=False, help='Allow dirty repository')
@click.option('-s', '--stash', 'stash', is_flag=True, default=False, help='No stashing')
def cli(dirty, stash):
    """
    This is a tool that handles all the tasks to build a Python application

    This tool is installed as a setuptools entry point, which means it should be accessible from your terminal once
    this application is installed in develop mode.
    """
    _setup_logging()

    LOGGER.info('EPAB %s', __version__)
    LOGGER.info('Running in %s', os.getcwd())

    CTX.repo = epab.utils.Repo()
    CTX.repo.ensure()
    CTX.stash = stash
    for filename in _GIT_IGNORE:
        epab.utils.add_to_gitignore(filename)
    if not dirty and CTX.repo.is_dirty():
        LOGGER.error('Repository is dirty')
        sys.exit(-1)


def _pre_push(ctx: click.core.Context, push: bool):
    if not sys.argv[0].endswith('__main__.py'):
        LOGGER.error('This command cannot be run as a script. Use this instead:\n\n\t'
                     'python -m epab (-d) pre_push')
        sys.exit(1)

    ctx.invoke(epab.cmd.pipenv_update)
    ctx.invoke(epab.cmd.pipenv_clean)
    ctx.invoke(epab.linters.lint)
    ctx.invoke(epab.cmd.pytest, long=True)
    ctx.invoke(epab.cmd.reqs)
    ctx.invoke(epab.cmd.pipenv_check)
    if push:
        CTX.repo.push()


@cli.command()
@click.pass_context
@click.option('-p', '--push', is_flag=True, default=False, help='Push to remote origin')
def pre_push(ctx, push: bool):
    """
    Runs a series of tests & checks before pushing to Git remote
    """
    _pre_push(ctx, push)


@cli.command()
@click.pass_context
@click.option('-p', '--push', is_flag=True, default=False, help='Push to remote origin')
def pp(ctx, push: bool):  # pylint: disable=invalid-name
    """
    Alias for "pre_push"
    """
    _pre_push(ctx, push)


_LINTERS = [
    # epab.linters.pep8,
    # epab.linters.flake8,
    # epab.linters.sort,
    epab.linters.pylint,
    epab.linters.safety,
    epab.linters.lint,
    epab.linters.mypy,
    epab.linters.pytest_dead_fixtures,
    epab.linters.bandit
]

_COMMANDS = [
    epab.cmd.reqs,
    epab.cmd.release,
    epab.cmd.chglog,
    epab.cmd.pytest,
    epab.cmd.install_hooks,
    epab.cmd.push,
    epab.cmd.freeze,
    epab.cmd.pipenv,
    epab.cmd.graph,
]

for command in _COMMANDS + _LINTERS:
    cli.add_command(command)

if __name__ == '__main__':
    cli(obj={})  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
