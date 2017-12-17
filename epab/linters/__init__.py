# coding=utf-8
"""
Manages linters
"""
import sys
from pathlib import Path
import click

from epab.utils import _info, do, repo_commit


@click.command()
@click.pass_context
def pep8(ctx):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    do(ctx, ['autopep8', '-r', '--in-place', '.'])


@click.command()
@click.pass_context
def flake8(ctx):
    """
    Runs Flake8 (http://flake8.pycqa.org/en/latest/)
    """
    ignore = ['--ignore=D203,E126']
    max_line_length = ['--max-line-length=120']
    # noinspection SpellCheckingInspection
    exclude = ['--exclude', '_version.py,_*_version.py,_versioneer.py,versioneer.py,.svn,CVS,.bzr,.hg,.git,'
                            '__pycache__,.tox,__init__.py,dummy_miz.py,build,dist,output,.cache,.hypothesis,'
                            'qt_resource.py,_parking_spots.py,./test/*,./.eggs/*,']
    max_complexity = ['--max-complexity=10']
    do(ctx, ['flake8'] + ignore + max_line_length + exclude + max_complexity)


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
@click.argument('src', type=click.Path(exists=True), default=None, required=False)
@click.option('-r', '--reports', is_flag=True, help='Display full report')
def pylint(ctx, src, reports):
    """
    Analyze a given python SRC (module or package) with Pylint (SRC must exist)

    Default module: CONFIG['package']
    """
    # noinspection SpellCheckingInspection
    ignore = ['--ignore=CVS,versioneer.py,_versioneer.py,_version.py',
              '--ignore-patterns=_.*_version']
    line_length = ['--max-line-length=120']
    jobs = ['-j', '2']
    persistent = ['--persistent=y']
    site_packages = str(Path(sys.executable).parent.parent.joinpath(
        'lib/site-packages')).replace('\\', '/')
    init_hook = [f'--init-hook=import sys; sys.path.append("{site_packages}")']
    disable = ['-d', 'disable=missing-docstring,logging-format-interpolation,unpacking-in-except,old-raise-syntax,'
                     'backtick,long-suffix,old-ne-operator,old-octal-literal,raw-checker-failed,bad-inline-option,'
                     'locally-disabled,locally-enabled,file-ignored,suppressed-message,useless-suppression,'
                     'deprecated-pragma,apply-builtin,basestring-builtin,buffer-builtin,cmp-builtin,coerce-builtin,'
                     'execfile-builtin,file-builtin,long-builtin,raw_input-builtin,reduce-builtin,'
                     'standarderror-builtin,unicode-builtin,xrange-builtin,coerce-method,delslice-method,'
                     'getslice-method,setslice-method,no-absolute-import,old-division,dict-iter-method,'
                     'dict-view-method,next-method-called,metaclass-assignment,indexing-exception,'
                     'raising-string,reload-builtin,oct-method,hex-method,nonzero-method,cmp-method,input-builtin,'
                     'round-builtin,intern-builtin,unichr-builtin,map-builtin-not-iterating,zip-builtin-not-iterating,'
                     'range-builtin-not-iterating,filter-builtin-not-iterating,using-cmp-argument,eq-without-hash,'
                     'div-method,idiv-method,rdiv-method,exception-message-attribute,invalid-str-codec,sys-max-int,'
                     'bad-python3-import,deprecated-string-function,deprecated-str-translate-call']
    evaluation = [
        '--evaluation=10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)']
    output = ['--output-format=text']
    report = ['--reports=n']
    score = ['--score=n']
    if src is None:
        src = ctx.obj['CONFIG']['package']
    cmd = ['pylint', src]
    if reports:
        report = ['--reports=y']
    do(ctx, cmd + ignore + line_length + jobs + persistent + init_hook +
       disable + evaluation + output + report + score)


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
    """
    Runs all linters
    Args:
        auto_commit: whether or not to commit results
    """
    _info('Running all linters')
    ctx.invoke(pep8)
    ctx.invoke(isort)
    ctx.invoke(flake8)
    ctx.invoke(pylint)
    # ctx.invoke(prospector)
    ctx.invoke(safety)
    if auto_commit:
        repo_commit(ctx, 'chg: dev: linting [auto] [skip ci]')
