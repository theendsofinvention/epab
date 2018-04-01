# coding=utf-8

from hypothesis import strategies as st, given
from epab.utils import _next_version as nv
from mockito import when, verifyStubbedInvocationsAreUsed, mock


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
    assert nv._get_calver() == f'{year}.{month}.{day}'
    verifyStubbedInvocationsAreUsed()

