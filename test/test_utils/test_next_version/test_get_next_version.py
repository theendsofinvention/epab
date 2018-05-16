# coding=utf-8
import pytest
from mockito import verifyStubbedInvocationsAreUsed, when

from epab.utils import _next_version, get_next_version

CALVER = '2018.1.2'


@pytest.fixture(autouse=True)
def _mock_calver():
    when(_next_version)._get_calver().thenReturn(CALVER)
    yield
    verifyStubbedInvocationsAreUsed()


def _check_next_version(repo, expected_version):
    next_version = get_next_version()
    assert expected_version == next_version
    repo.mark(f'calver: {CALVER}')
    repo.mark(f'next version: {next_version}')


def test_next_version_empty_repo(repo):
    assert not repo.list_tags()
    assert repo.get_current_branch() == 'master'
    _check_next_version(repo, f'{CALVER}.1')


def test_next_version_stable(repo):
    assert repo.get_current_branch() == 'master'
    repo.tag(f'{CALVER}.1')
    _check_next_version(repo, f'{CALVER}.2')


def test_next_version_stable_older_calver(repo):
    assert repo.get_current_branch() == 'master'
    repo.tag(f'2018.1.1.1')
    repo.tag(f'2018.1.1.2')
    _check_next_version(repo, f'{CALVER}.1')


@pytest.mark.long
def test_next_version_alpha_empty_repo(repo):
    assert repo.get_current_branch() == 'master'
    repo.create_branch_and_checkout('test')
    _check_next_version(repo, f'{CALVER}.1a1+test')


@pytest.mark.long
def test_next_version_alpha(repo):
    assert repo.get_current_branch() == 'master'
    repo.tag('2018.1.1.1')
    repo.tag('2018.1.1.2')
    _check_next_version(repo, f'{CALVER}.1')
    repo.tag(f'{CALVER}.1')
    repo.create_branch_and_checkout('test')
    repo.tag(f'{CALVER}.2a1+test')
    repo.tag(f'{CALVER}.2a2+test')
    _check_next_version(repo, f'{CALVER}.2a3+test')
    repo.checkout('master')
    _check_next_version(repo, f'{CALVER}.2')
