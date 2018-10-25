# coding=utf-8
"""
Manages the test suite
"""
import logging
import os
import shutil
import webbrowser
from pathlib import Path

import click
import elib_run

import epab.utils
from epab.core import CTX, config

LOGGER = logging.getLogger('EPAB')
PYTEST_OPTIONS = ' '.join([
    '--cov={package}',
    '--cov-report xml',
    '--cov-report html',
    '--cov-branch',
    # f'--cov-fail-under={CONFIG.test__coverage__fail_under}',
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
"""


class _Coverage:
    @staticmethod
    def install():
        """
        Installs coverage config file
        """
        Path('.coveragerc').write_text(COVERAGE_CONFIG.format(package_name=config.PACKAGE_NAME()))

    @staticmethod
    def upload_coverage_to_codacy():
        """
        Uploads the coverage to Codacy
        """
        if not Path('coverage.xml').exists():
            LOGGER.error('coverage.xml not found, skipping codacy coverage')
            return
        if os.getenv('CODACY_PROJECT_TOKEN') is None:
            LOGGER.error('CODACY_PROJECT_TOKEN env var not defined, skipping codacy coverage')
            return

        LOGGER.info('uploading coverage to Codacy')
        elib_run.run('pip install --upgrade codacy-coverage')
        elib_run.run('python-codacy-coverage -r coverage.xml')
        LOGGER.info('codacy coverage OK')

    # Disabled for the time being
    # @staticmethod
    # def upload_coverage_to_scrutinizer():
    #     """
    #     Uploads the coverage to Scrutinizer
    #     """
    #     if os.getenv('SCRUT_TOK', False):
    #         if Path('coverage.xml').exists():
    #             LOGGER.info('Uploading coverage to Scrutinizer')
    #             elib_run.run('pip install git+https://github.com/etcher-vault/ocular.py.git#egg=ocular')
    #             token = os.getenv('SCRUT_TOK')
    #             elib_run.run(
    #                 f'ocular --access-token "{token}" --data-file "coverage.xml" --config-file ".coveragerc"'
    #             )
    #             LOGGER.info('Scrutinizer coverage OK')
    #         else:
    #             LOGGER.error('"coverage.xml" not found, skipping ocular coverage')
    #     else:
    #         LOGGER.error('no "SCRUT_TOK" in environment, skipping ocular coverage')

    @staticmethod
    def remove_config_file():
        """
        Removes coverage config file
        """
        try:
            Path('.coveragerc').unlink()
        except FileNotFoundError:
            pass


def upload_coverage():
    """
    Sends coverage result to Codacy and Scrutinizer if running on AV
    """
    if CTX.appveyor:
        # _Coverage.upload_coverage_to_scrutinizer()
        _Coverage.upload_coverage_to_codacy()
    else:
        LOGGER.info('skipping coverage upload')


def pytest_options():
    """
    Returns: PyTest standard command line options
    """
    return PYTEST_OPTIONS.format(
        package=config.PACKAGE_NAME(),
        test_duration=config.TEST_DURATION_COUNT(),
    )


@epab.utils.run_once
@epab.utils.timeit
def _pytest(test, *, long, show, exitfirst, last_failed, failed_first, rm_cov):
    LOGGER.info('running test suite')
    os.environ['PYTEST_QT_API'] = 'pyqt5'
    _Coverage.install()
    cmd = f'pytest {test}'

    if CTX.appveyor:
        LOGGER.debug('running on AV; VCR recording disabled')
        cmd = f'{cmd} --vcr-record=none'

    if CTX.appveyor and config.TEST_AV_RUNNER_OPTIONS():
        cmd = f'{cmd} {config.TEST_AV_RUNNER_OPTIONS()}'
    elif config.TEST_RUNNER_OPTIONS():
        cmd = f'{cmd} {config.TEST_RUNNER_OPTIONS()}'

    long = ' --long' if long else ''
    exitfirst = ' --exitfirst' if exitfirst else ''
    last_failed = ' --last-failed' if last_failed else ''
    failed_first = ' --failed-first' if failed_first else ''

    if rm_cov and Path('./htmlcov').exists():
        shutil.rmtree('./htmlcov')
    cmd = f'{cmd} {pytest_options()}{long}{exitfirst}{last_failed}{failed_first}'

    try:
        elib_run.run(cmd, timeout=config.TEST_PYTEST_TIMEOUT())
    finally:
        upload_coverage()
        _Coverage.remove_config_file()
    if show:
        # noinspection SpellCheckingInspection
        path = Path('./htmlcov/index.html').absolute()
        webbrowser.open(f'file://{path}')


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('-l', '--long', is_flag=True, default=False, help='Long tests')
@click.option('-s', '--show', is_flag=True, default=False, help='Show coverage in browser')
@click.option('-x', '--exitfirst', is_flag=True, default=False, help='Exit instantly on first error')
@click.option('-r', '--rm-cov', is_flag=True, default=False, help='Delete coverage report from previous runs')
@click.option('-lf', '--last-failed', is_flag=True, default=False, help='Rerun only the tests that failed')
@click.option('-ff', '--failed-first', is_flag=True, default=False,
              help='Run all tests but run the last failures first')
@click.option('-t', '--test', default=config.TEST_TARGET(), help='Select which tests to run')
def pytest(test, long, show, exitfirst, last_failed, failed_first, rm_cov):
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
        rm_cov=rm_cov,
    )
