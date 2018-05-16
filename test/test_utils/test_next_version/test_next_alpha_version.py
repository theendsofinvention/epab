# coding=utf-8

import pytest

from epab.utils import _next_version as nv


def _check_next_version(repo, expected_version, calver):
    tags = nv._get_current_calver_tags(calver)
    next_version = nv._next_stable_version(calver, tags)
    next_alpha = nv._next_alpha_version(next_version, tags)
    assert expected_version == next_alpha
    repo.mark(f'next_version: {next_alpha}')


@pytest.mark.long
def test_next_alpha_version(repo):
    calver = '2018.1.1'
    repo.create_branch_and_checkout('test')
    _check_next_version(repo, f'{calver}.1a1+test', calver)


@pytest.mark.long
def test_next_alpha_version_with_existing_version(repo):
    calver = '2018.1.1'
    repo.tag(f'{calver}.1')
    repo.create_branch_and_checkout('test')
    _check_next_version(repo, f'{calver}.2a1+test', calver)


@pytest.mark.long
def test_next_stable_version_with_existing_mixed_version(repo):
    calver = '2018.1.1'
    repo.tag(f'{calver}.1')
    repo.tag(f'{calver}.2')
    repo.tag(f'{calver}.3')
    repo.create_branch_and_checkout('test')
    _check_next_version(repo, f'{calver}.4a1+test', calver)


@pytest.mark.long
def test_next_stable_version_with_existing_alpha(repo):
    calver = '2018.1.1'
    repo.create_branch_and_checkout('test')
    repo.tag(f'{calver}.1a1+test')
    repo.tag(f'{calver}.1a2+test')
    repo.tag(f'{calver}.1a3+test')
    _check_next_version(repo, f'{calver}.1a4+test', calver)


@pytest.mark.long
def test_next_stable_version_with_existing_mixed_alpha(repo):
    calver = '2018.1.1'
    repo.tag(f'{calver}.1')
    repo.tag(f'{calver}.2')
    repo.create_branch_and_checkout('test')
    repo.tag(f'{calver}.1a1+test')
    repo.tag(f'{calver}.1a2+test')
    repo.tag(f'{calver}.1a3+test')
    repo.tag(f'{calver}.2a1+test')
    repo.tag(f'{calver}.2a2+test')
    repo.tag(f'{calver}.2a3+test')
    repo.tag(f'{calver}.3a1+test')
    repo.tag(f'{calver}.3a2+test')
    repo.tag(f'{calver}.3a3+test')
    _check_next_version(repo, f'{calver}.3a4+test', calver)
