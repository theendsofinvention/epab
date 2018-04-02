# coding=utf-8
import pytest

from epab.utils import _next_version as nv


def _check_types(tag: nv.Tag):
    assert isinstance(tag.calver, str)
    assert isinstance(tag.quantifier, int)
    assert isinstance(tag.branch, str)
    assert isinstance(tag.alpha_quantifier, int)


def test_version_tag():
    tag = nv.Tag('2018.4.1.1')
    _check_types(tag)
    assert not tag.is_alpha
    assert '2018.4.1' == tag.calver
    assert 1 is tag.quantifier
    assert '' == tag.branch
    assert 0 == tag.alpha_quantifier


def test_version_tag_alpha():
    tag = nv.Tag('2018.4.1.1a2+test')
    _check_types(tag)
    assert tag.is_alpha
    assert '2018.4.1' == tag.calver
    assert 1 is tag.quantifier
    assert 'test' == tag.branch
    assert 2 == tag.alpha_quantifier


@pytest.mark.parametrize(
    'value',
    ['2018', '2018.1.4', '2018.1.1.1a1', '2018.1.1.1a']
)
def test_version_tag_wrong_value(value):
    with pytest.raises(ValueError):
        nv.Tag(value)


@pytest.mark.parametrize(
    'value',
    [2, -1, None, False]
)
def test_version_tag_wrong_type(value):
    with pytest.raises(TypeError):
        nv.Tag(value)
