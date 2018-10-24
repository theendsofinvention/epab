# coding=utf-8
"""
Pipenv helpers
"""

import click
from elib_run import run

import epab.utils


@epab.utils.timeit
def _pipenv(args: str):
    run('pipenv ' + args, mute=True, timeout=300)


@epab.utils.run_once
@epab.utils.timeit
def _check():
    _pipenv('check')


@epab.utils.run_once
@epab.utils.timeit
def _lock(dev: bool = True):
    _pipenv('lock' + ' --dev' if dev else '')


@epab.utils.run_once
@epab.utils.timeit
def _update(dev: bool = True):
    _pipenv('update' + ' --dev' if dev else '')


@epab.utils.run_once
@epab.utils.timeit
def _clean():
    _pipenv('clean')


@click.group(name='pipenv')
def pipenv():
    """
    Pipenv Click command group
    """


@pipenv.command()
def check():
    """
    Runs 'pipenv check'
    """
    _check()


@pipenv.command()
def clean():
    """
    Runs 'pipenv clean'
    """
    _clean()


@pipenv.command()
@click.option('-d', '--dev', is_flag=True, default=True, help='Include dev packages')
def update(dev):
    """
    Runs 'pipenv update'
    """
    _update(dev)


@pipenv.command()
@click.option('-d', '--dev', is_flag=True, default=True, help='Include dev packages')
def lock(dev):
    """
    Runs 'pipenv lock'
    """
    _lock(dev)
