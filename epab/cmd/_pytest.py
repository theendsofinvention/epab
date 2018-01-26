# coding=utf-8
"""
Manages the test suite
"""
import os
import webbrowser
from pathlib import Path

import click

import epab.utils
from epab.core import CONFIG

PYTEST_OPTIONS = ' '.join([
    '--cov={package}',
    '--cov-report xml',
    '--cov-report html',
    '--cov-branch',
    f'--cov-fail-under={CONFIG.test__coverage__fail_under}',
    '--durations={test_duration}',
    # '--hypothesis-show-statistics',
    '--tb=short',
    '--cov-config .coveragerc',
    # '--dead-fixtures',
    # '--dup-fixtures',
    # '-x',
])

# noinspection SpellCheckingInspection
COVERAGE_CONFIG = r"""
## http://coverage.readthedocs.io/en/latest/config.html
[run]
# timid = True
branch = True
source = epab
# omit =

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

    # Ignore click commands
    # @click.command()

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


class _CoverageConfigFile:
    @staticmethod
    def install():
        """
        Installs coverage config file
        """
        Path('.coveragerc').write_text(COVERAGE_CONFIG.format(package_name=CONFIG.package))

    @staticmethod
    def remove():
        """
        Removes coverage config file
        """
        Path('.coveragerc').unlink()


def pytest_options():
    """
    Returns: PyTest standard command line options
    """
    return PYTEST_OPTIONS.format(
        package=CONFIG.package,
        test_duration=CONFIG.test__duration,
    )


@epab.utils.run_once
def _pytest(test, *, long, show, exitfirst, last_failed, failed_first):
    epab.utils.info('Running test suite')
    os.environ['PYTEST_QT_API'] = 'pyqt5'
    _CoverageConfigFile.install()
    cmd = f'pytest {test}'
    if os.environ.get('APPVEYOR') and CONFIG.test__av_runner_options:
        cmd = f'{cmd} {CONFIG.test__av_runner_options}'
    elif CONFIG.test__runner_options:
        cmd = f'{cmd} {CONFIG.test__runner_options}'
    cmd = f'{cmd} {pytest_options()}'
    if long:
        cmd = f'{cmd} --long'
    if exitfirst:
        cmd = f'{cmd} --exitfirst'
    if last_failed:
        cmd = f'{cmd} --last-failed'
    if failed_first:
        cmd = f'{cmd} --failed-first'
    try:
        epab.utils.run(cmd)
    finally:
        _CoverageConfigFile.remove()
    if show:
        # noinspection SpellCheckingInspection
        path = Path('./htmlcov/index.html').absolute()
        webbrowser.open(f'file://{path}')


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('-l', '--long', is_flag=True, default=False, help='Long tests')
@click.option('-s', '--show', is_flag=True, default=False, help='Show coverage in browser')
@click.option('-x', '--exitfirst', is_flag=True, default=False, help='Exit instantly on first error')
@click.option('--lf', '--last-failed', is_flag=True, default=False, help='Rerun only the tests that failed')
@click.option('--ff', '--failed-first', is_flag=True, default=False,
              help='Run all tests but run the last failures first')
@click.option('-t', '--test', default=CONFIG.test__target, help='Select which tests to run')
def pytest(test, long, show, exitfirst, last_failed, failed_first):
    """
    Runs Pytest (https://docs.pytest.org/en/latest/)
    """
    _pytest(
        test,
        long=long,
        show=show,
        exitfirst=exitfirst,
        last_failed=last_failed,
        failed_first=failed_first,
    )
