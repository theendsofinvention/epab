# coding=utf-8
"""
Flake8 linter
"""

import click

import epab.utils


@epab.utils.run_once
def _pytest_dead_fixtures():
    epab.utils.run(f'pytest test --dead-fixtures --dup-fixtures', mute=True)


@click.command()
def pytest_dead_fixtures():
    """
    Runs Flake8 (http://flake8.pycqa.org/en/latest/)
    """
    _pytest_dead_fixtures()
