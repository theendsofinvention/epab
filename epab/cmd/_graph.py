# coding=utf-8
"""
Wrapper around pyreverse (needs Graphviz in the path)
"""
import logging
from pathlib import Path

import click
import elib_run

import epab.utils
from epab.core import config

LOGGER = logging.getLogger('EPAB')


@epab.utils.timeit
def _graph():
    out_files = [
        Path(f'packages_{config.PACKAGE_NAME()}.png').absolute(),
        Path(f'classes_{config.PACKAGE_NAME()}.png').absolute(),
    ]
    for _file in out_files:
        if _file.exists:
            logging.debug('removing graph file: %s', _file)

    elib_run.run(f'pyreverse -o png -p {config.PACKAGE_NAME()} {config.PACKAGE_NAME()}')
    if any((file.exists() for file in out_files)):
        out_dir = Path('graphs')
        out_dir.mkdir(exist_ok=True)
        for file in out_files:
            if file.exists():
                file.rename(f'{file.parent}/graphs/{file.name}')


@click.command()
def graph():
    """
    Creates a graphical representation of the package inheritance & import trees
    """
    _graph()
