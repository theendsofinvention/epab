# coding=utf-8
import pytest
from hypothesis import given, strategies as st
from mockito import mock, verifyStubbedInvocationsAreUsed, when

from epab.utils import _next_version as nv


@pytest.mark.long
@given(
    year=st.integers(min_value=1950, max_value=8000),
    month=st.integers(min_value=1, max_value=12),
    day=st.integers(min_value=1, max_value=31)
)
def test_calver(year, month, day):
    now = mock()
    now.year = year
    now.month = month
    now.day = day
    when(nv)._get_datetime().thenReturn(now)
    assert nv._get_calver() == f'{year}.{month:02d}.{day:02d}'
    verifyStubbedInvocationsAreUsed()
