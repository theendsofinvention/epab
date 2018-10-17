# coding=utf-8

import itertools
import subprocess
from pathlib import Path

import elib_run
import pytest
from mockito import mock, verify, verifyNoMoreInteractions, verifyStubbedInvocationsAreUsed, when

import epab.utils
from epab.core import CTX, config
# noinspection PyProtectedMember
from epab.linters import _bandit, _dead_fixtures, _flake8, _lint, _mypy, _pep8, _pylint, _safety, _sort


@pytest.fixture(autouse=True, name='repo')
def _all():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    yield repo


def _check_invocations(context, amend, stage):
    assert isinstance(amend, bool)
    assert isinstance(stage, bool)
    verify(context).invoke(_safety.safety)
    verify(context).invoke(_pylint.pylint)
    verify(context).invoke(_flake8.flake8)
    verify(context).invoke(_mypy.mypy)
    verify(context).invoke(_bandit.bandit)
    verify(context).invoke(_dead_fixtures.pytest_dead_fixtures)
    # verify(context).invoke(_sort.sort, amend=amend, stage=stage)
    # verify(context).invoke(_pep8.pep8, amend=amend, stage=stage)
    verifyNoMoreInteractions(context)


@pytest.mark.parametrize(
    'amend_stage',
    itertools.product([False, True], repeat=2),
)
def test_lint(amend_stage):
    amend, stage = amend_stage
    context = mock()
    _lint._lint(context, amend, stage)
    _check_invocations(context, amend, stage)


@pytest.mark.parametrize(
    'amend_stage',
    itertools.product([False, True], repeat=2),
)
def test_lint_appveyor(amend_stage):
    amend, stage = amend_stage
    CTX.appveyor = True
    when(subprocess).call('appveyor AddMessage "running: _lint" -Category Information')
    when(subprocess).call(
        f'appveyor AddMessage "running all linters; stage: {stage}; amend: {amend}" -Category Information'
    )
    context = mock()
    _lint._lint(context, amend, stage)
    _check_invocations(context, amend, stage)


def test_isort_package_dir():
    Path(f'./{config.PACKAGE_NAME()}').mkdir()
    test_file = Path(f'./{config.PACKAGE_NAME()}/test.py')
    test_file.touch()
    when(_sort)._sort_file(test_file.absolute())
    _sort._sort()
    verifyStubbedInvocationsAreUsed()


def test_isort_test_dir():
    Path('./test').mkdir()
    test_file = Path('./test/test.py')
    test_file.touch()
    when(_sort)._sort_file(test_file.absolute())
    _sort._sort()
    verifyStubbedInvocationsAreUsed()


def test_isort_ignore():
    test_file = Path('./test.py')
    test_file.touch()
    when(_sort.isort).SortImports(
        file_path=test_file.absolute(),
        known_first_party=config.PACKAGE_NAME(),
        **_sort.SETTINGS
    )
    # when(elib_run).run(contains('setup.py isort'))
    _sort._sort()
    verify(_sort.isort, times=0).SortImports(...)


def test_isort_amend():
    # when(elib_run).run(contains('setup.py isort'))
    when(CTX.repo).amend_commit(append_to_msg='sorting imports [auto]')
    _sort._sort(amend=True)
    verifyStubbedInvocationsAreUsed()


def test_isort_stage():
    when(CTX.repo).stage_all()
    _sort._sort(stage=True)
    verifyStubbedInvocationsAreUsed()


def test_flake8():
    base_cmd = ' '.join((_flake8.IGNORE, _flake8.MAX_LINE_LENGTH, _flake8.EXCLUDE, _flake8.MAX_COMPLEXITY))
    when(elib_run).run(f'flake8 {base_cmd}', mute=True)
    _flake8._flake8()
    verifyStubbedInvocationsAreUsed()


def test_safety():
    when(elib_run).run('safety check --bare', mute=True)
    _safety._safety()
    verifyStubbedInvocationsAreUsed()


@pytest.mark.parametrize(
    'params,cmd',
    [
        ((None, True), 'pylint ./test --reports=y'),
        ((None, False), 'pylint ./test --reports=n'),
        (('src', False), 'pylint src --reports=n'),
    ]
)
def test_pylint(params, cmd):
    config.PACKAGE_NAME.default = 'test'
    with when(elib_run).run(f'{cmd} {_pylint.BASE_CMD}', mute=True):
        _pylint._pylint(*params)
        verify(elib_run).run(...)


def test_dead_fixtures():
    when(elib_run).run('pytest test --dead-fixtures --dup-fixtures', mute=True)
    _dead_fixtures._pytest_dead_fixtures()
    verifyStubbedInvocationsAreUsed()


def test_bandit():
    when(elib_run).run('bandit test_package -r', mute=True)
    _bandit._bandit()
    verifyStubbedInvocationsAreUsed()


def test_mypy():
    when(elib_run).run('mypy -p test_package --ignore-missing-imports', failure_ok=True).thenReturn(('', 0))
    _mypy._mypy()
    verifyStubbedInvocationsAreUsed()


def test_mypy_fails():
    when(elib_run).run('mypy -p test_package --ignore-missing-imports', failure_ok=True).thenReturn(('', 1))
    with pytest.raises(SystemExit):
        _mypy._mypy()
    verifyStubbedInvocationsAreUsed()


def test_mypy_config():
    config.MYPY_ARGS.default = 'some --params'
    when(elib_run).run(
        'mypy -p test_package --ignore-missing-imports some --params', failure_ok=True
    ).thenReturn(('', 0))
    _mypy._mypy()
    verifyStubbedInvocationsAreUsed()
