# coding=utf-8
"""
Flake8 linter
"""

import click
import epab.utils


@epab.utils.run_once
def _flake8(ctx):
    ignore = ['--ignore=D203,E126']
    max_line_length = ['--max-line-length=120']
    # noinspection SpellCheckingInspection
    exclude = ['--exclude', '_version.py,_*_version.py,_versioneer.py,versioneer.py,.svn,CVS,.bzr,.hg,.git,'
                            '__pycache__,.tox,__init__.py,dummy_miz.py,build,dist,output,.cache,.hypothesis,'
                            'qt_resource.py,_parking_spots.py,./test/*,./.eggs/*,']
    max_complexity = ['--max-complexity=10']
    epab.utils.do(ctx, ['flake8'] + ignore + max_line_length + exclude + max_complexity)


@click.command()
@click.pass_context
def flake8(ctx):
    """
    Runs Flake8 (http://flake8.pycqa.org/en/latest/)
    """
    _flake8(ctx)
