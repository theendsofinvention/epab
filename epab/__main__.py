# coding=utf-8

# coding=utf-8
"""
Collections of tools to build a python app
"""
import os
import sys

import click

import epab.cmd
import epab.linters
import epab.utils
from epab.core import CONFIG, CTX, VERSION


@click.group(chain=True)
@click.option('-v', '--version',
              is_flag=True, is_eager=True, expose_value=False, callback=epab.cmd.print_version, default=False,
              help='Print version and exit')
@click.option('-nv', '--next-version',
              is_flag=True, is_eager=True, expose_value=False, callback=epab.cmd.next_version, default=False,
              help='Print next version and exit')
@click.option('-n', '--dry-run', is_flag=True, default=False, help='Dry run')
@click.option('-d', '--dirty', is_flag=True, default=False, help='Allow dirty repository')
@click.option('-s', '--stash', 'stash', is_flag=True, default=False, help='No stashing')
def cli(dry_run, dirty, stash):
    """
    This is a tool that handles all the tasks to build a Python application

    This tool is installed as a setuptools entry point, which means it should be accessible from your terminal once
    this application is installed in develop mode.

    Just activate your venv and type the following in whatever shell you fancy:
    """
    epab.utils.info(f'EPAB {VERSION}')
    epab.utils.info(f'Running in {os.getcwd()}')
    CONFIG.load()
    CTX.dry_run = dry_run
    CTX.repo = epab.utils.Repo()
    CTX.repo.ensure()
    CTX.stash = stash
    if not dirty and CTX.repo.is_dirty():
        click.secho('Repository is dirty', err=True, fg='red')
        sys.exit(-1)


_LINTERS = [
    epab.linters.pep8,
    epab.linters.flake8,
    epab.linters.sort,
    epab.linters.pylint,
    epab.linters.safety,
    epab.linters.lint,
]

_COMMANDS = [
    epab.cmd.reqs,
    epab.cmd.release,
    epab.cmd.chglog,
    epab.cmd.pytest,
    epab.cmd.install_hooks,
    epab.cmd.push,
    epab.cmd.freeze,
    epab.cmd.flat_freeze,
]

for command in _COMMANDS + _LINTERS:
    cli.add_command(command)

if __name__ == '__main__':
    cli(obj={})  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
