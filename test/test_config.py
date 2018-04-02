# coding=utf-8

import string
import sys
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

# noinspection PyProtectedMember
from epab.core.config import TEST_VALUES, _Config, _ConfigProp


def test_mandatory_with_default_error():
    with pytest.raises(RuntimeError):
        _ConfigProp(mandatory=True, default='test')


def test_mandatory_missing():
    attribs = dict(
        mandatory_value=_ConfigProp(mandatory=True)
    )
    cls = type('DummyConfig', (_Config,), attribs)
    with pytest.raises(ValueError):
        cls().load()


@pytest.mark.parametrize(
    'caster,default',
    [
        (bool, True),
        (str, 'test'),
        (str, ''),
        (list, ['test', 'test']),
        (int, 0),
        (int, 1),
        (int, -1),
    ]
)
def test_dummy_config(caster, default):
    attribs = dict(
        value_without_default=_ConfigProp(cast=caster),
        value_with_default=_ConfigProp(cast=caster, default=default),
    )
    cls = type('DummyConfig', (_Config,), attribs)
    instance = cls()

    value_with_default = instance.value_with_default
    assert isinstance(value_with_default, caster)
    assert value_with_default == default

    value_without_default = instance.value_without_default
    assert not isinstance(value_without_default, caster)
    assert value_without_default is None

    instance.value_without_default = default
    value_without_default = instance.value_without_default
    assert value_without_default == default
    assert isinstance(value_without_default, caster)


def _run_casting_test(value, caster):
    attribs = dict(
        value=_ConfigProp(cast=caster, default=value),
    )
    cls = type('DummyConfig', (_Config,), attribs)
    instance = cls()
    assert isinstance(instance.value, caster)
    # noinspection PyUnresolvedReferences
    assert isinstance(cls.value, _ConfigProp)
    # noinspection PyUnresolvedReferences
    cls.value.default = None
    assert instance.value is None
    return instance


@given(value=st.text(alphabet=string.printable))
@pytest.mark.parametrize('caster', [str])
def test_with_text(value, caster):
    _run_casting_test(value, caster)


@given(value=st.booleans())
@pytest.mark.parametrize('caster', [bool])
def test_with_bool(value, caster):
    _run_casting_test(value, caster)


@given(value=st.lists(st.randoms()))
@pytest.mark.parametrize('caster', [list])
def test_with_list(value, caster):
    _run_casting_test(value, caster)


@given(value=st.integers())
@pytest.mark.parametrize('caster', [int])
def test_with_int(value, caster):
    _run_casting_test(value, caster)


@given(value=st.floats())
@pytest.mark.parametrize('caster', [float])
def test_with_float(value, caster):
    _run_casting_test(value, caster)


@given(value=st.dictionaries(keys=st.text(alphabet=string.ascii_lowercase), values=st.integers()))
@pytest.mark.parametrize('caster', [dict])
def test_with_dict(value, caster):
    instance = _run_casting_test(value, caster)
    instance.value = value
    for key, value in instance.value.items():
        assert isinstance(key, str)
        assert isinstance(value, int)


TEMPLATE_FILE = """
mandatory: exist
string_no_cast: string
bool: True
list_of_bool:
  - True
  - False
very:
  deeply:
    nested:
      variable: test
"""


@pytest.fixture(name='instance_from_file', scope='session')
def _dummy_config_from_file():
    config_file = Path('test.yml')
    config_file.write_text(TEMPLATE_FILE, 'utf8')
    attribs = dict(
        should_be_none=_ConfigProp(cast=bool),
        string_no_cast=_ConfigProp(),
        mandatory=_ConfigProp(mandatory=True),
        bool=_ConfigProp(cast=bool),
        list_of_bool=_ConfigProp(cast=list),
        very__deeply__nested__variable=_ConfigProp(),
    )
    cls = type('DummyConfig', (_Config,), attribs)
    instance = cls()
    instance.load(config_file=config_file.absolute())
    yield instance
    config_file.unlink()


def test_with_file_none(instance_from_file):
    assert instance_from_file.should_be_none is None


def test_with_file_mandatory(instance_from_file):
    assert instance_from_file.mandatory == 'exist'


def test_with_file_streing_no_cast(instance_from_file):
    assert isinstance(instance_from_file.string_no_cast, str)
    assert instance_from_file.string_no_cast == 'string'


def test_with_file_bool(instance_from_file):
    assert isinstance(instance_from_file.bool, bool)
    assert instance_from_file.bool is True


def test_with_file_list_of_bool(instance_from_file):
    assert isinstance(instance_from_file.list_of_bool, list)
    assert instance_from_file.list_of_bool == [True, False]


def test_with_file_nested(instance_from_file):
    assert instance_from_file.very__deeply__nested__variable == 'test'
    instance_from_file.very__deeply__nested__variable = 'caribou'
    assert instance_from_file.very__deeply__nested__variable == 'caribou'


def test_missing_config_file():
    instance = _Config()
    instance.load()
    assert instance._data == TEST_VALUES
    delattr(sys, '_called_from_test')
    with pytest.raises(FileNotFoundError):
        instance.load()
    setattr(sys, '_called_from_test', True)
