# coding=utf-8
import pytest

from epab.utils import _next_version as nv


@pytest.mark.long
def _check_next_version(repo, expected_version, calver):
    tags = nv._get_current_calver_tags(calver)
    next_version = nv._next_stable_version(calver, tags)
    assert expected_version == next_version
    repo.mark(f'next_version: {next_version}')


@pytest.mark.long
def test_next_stable_version(repo):
    calver = '2018.1.1'
    _check_next_version(repo, f'{calver}.1', calver)


@pytest.mark.long
def test_next_stable_version_with_existing_version(repo):
    calver = '2018.1.1'
    repo.tag(f'{calver}.1')
    _check_next_version(repo, f'{calver}.2', calver)


@pytest.mark.long
def test_next_stable_version_with_existing_mixed_version(repo):
    calver = '2018.1.1'
    repo.tag(f'{calver}.1')
    repo.tag(f'{calver}.2')
    repo.tag(f'{calver}.3')
    _check_next_version(repo, f'{calver}.4', calver)


@pytest.mark.long
def test_next_stable_version_with_existing_alpha(repo):
    calver = '2018.1.1'
    repo.tag(f'{calver}.1a1+branch')
    repo.tag(f'{calver}.1a2+branch')
    repo.tag(f'{calver}.1a3+branch')
    _check_next_version(repo, f'{calver}.1', calver)


@pytest.mark.long
def test_next_stable_version_with_existing_mixed_alpha(repo):
    calver = '2018.1.1'
    repo.tag(f'{calver}.1')
    repo.tag(f'{calver}.2')
    repo.tag(f'{calver}.3')
    repo.tag(f'{calver}.1a1+branch')
    repo.tag(f'{calver}.1a2+branch')
    repo.tag(f'{calver}.1a3+branch')
    repo.tag(f'{calver}.2a1+branch')
    repo.tag(f'{calver}.2a2+branch')
    repo.tag(f'{calver}.2a3+branch')
    repo.tag(f'{calver}.3a1+branch')
    repo.tag(f'{calver}.3a2+branch')
    repo.tag(f'{calver}.3a3+branch')
    _check_next_version(repo, f'{calver}.4', calver)


@pytest.mark.long
def test_mismatched_tags(repo):
    repo.tag('test')
    repo.tag('0.3.34')
    repo.tag('0.3.34a+some_branch1')
    repo.tag('0.3.34a+some_branch2')
    repo.tag('0.3.34a+some_branch3')
    calver = '2018.1.1'
    tags = nv._get_current_calver_tags(calver)
    assert nv._next_stable_version(calver, tags) == f'{calver}.1'
    repo.tag(f'{calver}.1')
    tags = nv._get_current_calver_tags(calver)
    assert nv._next_stable_version(calver, tags) == f'{calver}.2'
