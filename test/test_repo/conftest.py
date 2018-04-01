# coding=utf-8

from pathlib import Path

import pytest

import epab.utils


class _CTX:
    obj = {'dry_run': False}


def pytest_collection_modifyitems(items):
    for item in items:
        if 'test_repo/' in item.nodeid:
            item.add_marker(pytest.mark.long)


@pytest.fixture()
def repo(dummy_git_repo):
    dummy_git_repo.create()
    _repo = epab.utils.Repo()
    yield _repo


@pytest.fixture(params=[[f'DUMMY_FILE_{x}' for x in range(5)] for _ in range(1)])
def file_set(request):
    file_set_ = list(map(Path, request.param))
    for file in file_set_:
        file.touch()
    yield file_set_
