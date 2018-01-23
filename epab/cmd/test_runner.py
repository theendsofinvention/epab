# coding=utf-8
"""
Manages the test suite
"""
import os
from pathlib import Path

import click
import epab.utils


COVERAGE_CONFIG = r"""
## http://coverage.readthedocs.io/en/latest/config.html
[run]
#timid = True
branch = True
source = epab
omit =
    */_versioneer.py
    {package_name}/_version.py

[report]
# Regexes for lines to exclude from consideration
exclude_lines =
    # Have to re-enable the standard pragma
    pragma: no cover

    # Don't complain about missing debug-only code:
    def __repr__
    if self\.debug

    # Don't complain if tests don't hit defensive assertion code:
    raise AssertionError
    raise NotImplementedError
    pass

    # Ignore abstract definitions:
    @abc.abstractmethod
    @abc.abstractproperty

    # Don't complain if non-runnable code isn't run:
    if 0:
    if __name__ == .__main__.:

[html]
directory = ./htmlcov
title = Coverage report

[paths]
source=
    ./epab
"""


@epab.utils.run_once
def _run_tests(ctx, long):
    epab.utils.info('Running test suite')
    os.environ['PYTEST_QT_API'] = 'pyqt5'
    coverage_rc = Path('.coveragerc')
    coverage_rc.write_text(COVERAGE_CONFIG.format(package_name=ctx.obj["CONFIG"]["package"]))
    cmd = ['pytest', 'test']
    if os.environ.get('APPVEYOR') and ctx.obj['CONFIG']['test']['av_runner_options']:
        cmd = cmd + ctx.obj['CONFIG']['test']['av_runner_options']
    elif ctx.obj['CONFIG']['test']['runner_options']:
        cmd = cmd + ctx.obj['CONFIG']['test']['runner_options']
    options = [f'--cov={ctx.obj["CONFIG"]["package"]}', '--cov-report', 'xml', '--cov-report', 'html', '--durations=10',
               '--hypothesis-show-statistics', '--tb=short', '--cov-config', '.coveragerc']
    if long:
        options.append('--long')
    try:
        epab.utils.do(ctx, cmd + options)
    finally:
        coverage_rc.unlink()


@click.command()
@click.option('-l', '--long', is_flag=True, default=False, help='Long tests')
@click.pass_context
def pytest(ctx, long):
    """
    Runs Pytest (https://docs.pytest.org/en/latest/)
    """
    _run_tests(ctx, long)
