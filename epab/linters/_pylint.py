# coding=utf-8
"""
Pylint linter
"""


import sys
from pathlib import Path

import click
import epab.utils


@epab.utils.run_once
def _pylint(ctx, src, reports):
    # noinspection SpellCheckingInspection
    ignore = ['--ignore=CVS,versioneer.py,_versioneer.py,_version.py',
              '--ignore-patterns=_.*_version']
    line_length = ['--max-line-length=120']
    jobs = ['-j', '8']
    persistent = ['--persistent=y']
    site_packages = str(Path(sys.executable).parent.parent.joinpath(
        'lib/site-packages')).replace('\\', '/')
    init_hook = [f'--init-hook=import sys; sys.path.append("{site_packages}")']
    disable = ['-d', 'disable=logging-format-interpolation,fixme,'
                     'backtick,long-suffix,raw-checker-failed,bad-inline-option,'
                     'locally-disabled,locally-enabled,suppressed-message,'
                     'coerce-method,delslice-method,getslice-method,setslice-method,'
                     'next-method-called,too-many-arguments,too-few-public-methods,'
                     'reload-builtin,oct-method,hex-method,nonzero-method,cmp-method,'
                     'using-cmp-argument,eq-without-hash,exception-message-attribute,sys-max-int,'
                     'bad-python3-import,ungrouped-imports,wrong-import-order,']
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
    epab.utils.do(ctx, cmd + ignore + line_length + jobs + persistent + init_hook +
                  disable + evaluation + output + report + score)


@click.command()
@click.pass_context
@click.argument('src', type=click.Path(exists=True), default=None, required=False)
@click.option('-r', '--reports', is_flag=True, help='Display full report')
def pylint(ctx, src, reports):
    """
    Analyze a given python SRC (module or package) with Pylint (SRC must exist)

    Default module: CONFIG['package']
    """
    _pylint(ctx, src, reports)
