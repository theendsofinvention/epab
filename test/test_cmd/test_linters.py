# coding=utf-8

import itertools
from pathlib import Path

import pytest
from mockito import mock, verify, verifyNoMoreInteractions, verifyStubbedInvocationsAreUsed, when

import epab.utils
from epab.core import CONFIG, CTX
from epab.linters import _flake8, _lint, _pep8, _pylint, _safety, _sort


@pytest.fixture(autouse=True, name='repo')
def _all():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    yield repo


@pytest.mark.parametrize(
    'amend_stage',
    itertools.product([False, True], repeat=2),
)
def test_lint(amend_stage):
    amend, stage = amend_stage
    context = mock()
    _lint._lint(context, amend, stage)
    verify(context).invoke(_safety.safety)
    verify(context).invoke(_pylint.pylint)
    verify(context).invoke(_flake8.flake8)
    verify(context).invoke(_sort.sort, amend=amend, stage=stage)
    verify(context).invoke(_pep8.pep8, amend=amend, stage=stage)
    verifyNoMoreInteractions(context)


@pytest.mark.parametrize(
    'amend_stage',
    itertools.product([False, True], repeat=2),
)
def test_lint_appveyor(amend_stage):
    amend, stage = amend_stage
    CTX.appveyor = True
    context = mock()
    _lint._lint(context, amend, stage)
    verify(context).invoke(_safety.safety)
    verify(context).invoke(_pylint.pylint)
    verify(context).invoke(_flake8.flake8)
    verify(context).invoke(_pep8.pep8, amend=amend, stage=stage)
    verifyNoMoreInteractions(context)


def test_pep8():
    when(epab.utils).run(
        f'autopep8 -r --in-place --max-line-length {CONFIG.lint__line_length} {CONFIG.package}', mute=True)
    when(epab.utils).run(f'autopep8 -r --in-place --max-line-length {CONFIG.lint__line_length} test', mute=True)
    _pep8._pep8()
    verifyStubbedInvocationsAreUsed()


def test_pep8_amend():
    with when(CTX.repo).amend_commit(append_to_msg='pep8 [auto]'):
        CTX.run_once = {}
        _pep8._pep8(amend=True)
        verify(CTX.repo).amend_commit(...)


def test_pep8_stage():
    when(epab.utils).run(
        f'autopep8 -r --in-place --max-line-length {CONFIG.lint__line_length} {CONFIG.package}', mute=True)
    when(epab.utils).run(f'autopep8 -r --in-place --max-line-length {CONFIG.lint__line_length} test', mute=True)
    with when(CTX.repo).stage_all():
        CTX.run_once = {}
        _pep8._pep8(stage=True)
    verifyStubbedInvocationsAreUsed()


def test_isort():
    test_file = Path('./test.py')
    test_file.touch()
    when(_sort.isort).SortImports(
        file_path=test_file.absolute(),
        known_first_party=CONFIG.package,
        **_sort.SETTINGS
    )
    # when(epab.utils).run(contains('setup.py isort'))
    _sort._sort()
    verifyStubbedInvocationsAreUsed()


def test_isort_amend():
    # when(epab.utils).run(contains('setup.py isort'))
    when(CTX.repo).amend_commit(append_to_msg='sorting imports [auto]')
    _sort._sort(amend=True)
    verifyStubbedInvocationsAreUsed()


def test_isort_stage():
    # when(epab.utils).run(contains('setup.py isort'))
    when(CTX.repo).stage_all()
    _sort._sort(stage=True)
    verifyStubbedInvocationsAreUsed()


def test_flake8():
    base_cmd = ' '.join((_flake8.IGNORE, _flake8.MAX_LINE_LENGTH, _flake8.EXCLUDE, _flake8.MAX_COMPLEXITY))
    when(epab.utils).run(f'flake8 {base_cmd}', mute=True)
    _flake8._flake8()
    verifyStubbedInvocationsAreUsed()


def test_safety():
    when(epab.utils).run('safety check --bare', mute=True)
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
    CONFIG.load()
    CONFIG.package = 'test'
    with when(epab.utils).run(f'{cmd} {_pylint.BASE_CMD}', mute=True):
        _pylint._pylint(*params)
        verify(epab.utils).run(...)
