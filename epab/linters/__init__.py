# coding=utf-8

import click

from epab.utils import _info, do, repo_commit


@click.command()
@click.pass_context
def autopep8(ctx):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    do(ctx, ['autopep8', '-r', '--in-place', '.'])


@click.command()
@click.pass_context
def pep(ctx):
    ctx.invoke(autopep8)


@click.command()
@click.pass_context
def pep8(ctx):
    ctx.invoke(autopep8)


@click.command()
@click.pass_context
def flake8(ctx):
    """
    Runs Flake8 (http://flake8.pycqa.org/en/latest/)
    """
    do(ctx, ['flake8'])


@click.command()
@click.pass_context
def prospector(ctx):
    """
    Runs Landscape.io's Prospector (https://github.com/landscapeio/prospector)

    This includes flake8 & Pylint
    """
    do(ctx, ['prospector'])


@click.command()
@click.pass_context
def isort(ctx):
    """
    Runs iSort (https://pypi.python.org/pypi/isort)
    """
    do(ctx, ['isort', '-rc', '-w', '120', '-s', 'versioneer.py', '.'])


@click.command()
@click.pass_context
@click.argument('src', type=click.Path(exists=True), default=None)
@click.option('-r', '--reports', is_flag=True, help='Display full report')
def pylint(ctx, src, reports):
    """
    Analyze a given python SRC (module or package) with Pylint (SRC must exist)

    Default module: CONFIG['package']
    """
    if src is None:
        src = ctx.obj['CONFIG']['package']
    cmd = ['pylint', src]
    if reports:
        cmd.append('--reports=y')
    do(ctx, cmd)


@click.command()
@click.pass_context
def safety(ctx):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    do(ctx, ['safety', 'check', '--bare'])


@click.command()
@click.pass_context
@click.option('-c', '--auto-commit', is_flag=True, help='Commit the changes')
def lint(ctx: click.Context, auto_commit: bool):
    _info('Running all linters')
    ctx.invoke(autopep8)
    ctx.invoke(isort)
    ctx.invoke(flake8)
    ctx.invoke(pylint)
    # ctx.invoke(prospector)
    ctx.invoke(safety)
    if auto_commit:
        repo_commit(ctx, 'chg: dev: linting [auto] [skip ci]')
