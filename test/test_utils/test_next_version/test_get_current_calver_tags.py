# coding=utf-8
import pytest

import epab.utils
from epab.utils import _next_version as nv


@pytest.mark.long
def test_get_current_calver_tags(repo: epab.utils.Repo):
    calver = '2018.1.1'
    assert len(nv._get_current_calver_tags(calver)) == 0
    repo.tag(f'{calver}.1')
    assert len(nv._get_current_calver_tags(calver)) == 1
    repo.tag(f'{calver}.2')
    assert len(nv._get_current_calver_tags(calver)) == 2
