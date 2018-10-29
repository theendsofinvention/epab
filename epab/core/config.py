# coding=utf-8
"""
Handles EPAB's config file
"""

import logging
import pathlib

import elib_config

CHANGELOG_DISABLE = elib_config.ConfigValueBool(
    'changelog', 'disable', description='Disable changelog building', default=False
)
CHANGELOG_FILE_PATH = elib_config.ConfigValuePath(
    'changelog', 'file_path', description='Path to changelog file', default='CHANGELOG.md'
)
CHANGELOG_FILE_PATH.must_be_file()
TEST_RUNNER_OPTIONS = elib_config.ConfigValueString(
    'test', 'runner_options', description='Additional options for test run', default=''
)
TEST_DURATION_COUNT = elib_config.ConfigValueInteger(
    'test', 'duration_count', description='Amount of "slow" tests to show', default=10
)
TEST_DURATION_COUNT.set_limits(min_=0, max_=50)

TEST_TARGET = elib_config.ConfigValueString(
    'test', 'target', description='Target of pytest', default='test'
)

TEST_COVERAGE_FAIL_UNDER = elib_config.ConfigValueInteger(
    'test', 'coverage_fail_under', description='Minimal coverage to pass tests', default=20
)
TEST_COVERAGE_FAIL_UNDER.set_limits(min_=0, max_=100)
TEST_PYTEST_TIMEOUT = elib_config.ConfigValueInteger(
    'test', 'timeout', description='Timeout in seconds for pytest runner', default=300
)
TEST_PYTEST_TIMEOUT.set_limits(min_=0, max_=3600)

LINT_LINE_LENGTH = elib_config.ConfigValueInteger(
    'lint', 'line_length', description='Linter max line width', default=120
)
LINT_LINE_LENGTH.set_limits(min_=0, max_=500)

PACKAGE_NAME = elib_config.ConfigValueString(
    'package_name', description='Package name'
)

FREEZE_ENTRY_POINT = elib_config.ConfigValueString(
    'freeze', 'entry_point', description='Main entry point for pyinstaller', default=''
)
FREEZE_DATA_FILES = elib_config.ConfigValueList(
    'freeze', 'data_files', description='PyInstaller data-files list', element_type=str, default=[]
)

DOC_REPO = elib_config.ConfigValueString(
    'doc', 'repo', description='Documentation repository on Github', default=''
)
DOC_FOLDER = elib_config.ConfigValuePath(
    'doc', 'folder', description='Local documentation directory', default='./doc'
)
DOC_FOLDER.must_be_dir()

QUIET = elib_config.ConfigValueBool(
    'quiet', description='Less console output', default=False
)
VERBOSE = elib_config.ConfigValueBool(
    'verbose', description='More console output', default=False
)

TEST_AV_RUNNER_OPTIONS = elib_config.ConfigValueString(
    'appveyor', 'test_runner_options', description='Additional command line options for tests run on AV',
    default='--long'
)
ARTIFACTS = elib_config.ConfigValueList(
    'appveyor', 'artifacts', description='List of artifacts for Appveyor', element_type=str, default=[]
)
FLAKE8_EXCLUDE = elib_config.ConfigValueString(
    'lint', 'flake8_exclude', description='List of comma separated files for flake8 to exclude', default=''
)
MYPY_ARGS = elib_config.ConfigValueString(
    'lint', 'mypy_args', description='Additional MyPy arguments', default=''
)
QT_RES_SRC = elib_config.ConfigValueString(
    'qt', 'res_src', description='Qt resource file (.qrc) location', default=''
)
QT_RES_TGT = elib_config.ConfigValueString(
    'qt', 'res_tgt', description='Compiled Qt resource file (.py) target location', default=''
)
UPLOAD_TO_TWINE = elib_config.ConfigValueBool(
    'twine', 'upload', description='Upload package to Twine after build',
    default=True,
)
MAKE_GRAPH = elib_config.ConfigValueBool(
    'graph', 'make',
    description='Generate graphs using PyReverse',
    default=True,
)


def setup_config(epab_version: str):
    """
    Set up elib_config package

    :param epab_version: installed version of EPAB as as string
    """
    logger = logging.getLogger('EPAB')
    logger.debug('setting up config')
    elib_config.ELIBConfig.setup(
        app_name='EPAB',
        app_version=epab_version,
        config_file_path='pyproject.toml',
        config_sep_str='__',
        root_path=['tool', 'epab']
    )
    elib_config.write_example_config('pyproject.toml.example')
    if not pathlib.Path('pyproject.toml').exists():
        raise FileNotFoundError('pyproject.toml')
    elib_config.validate_config()
