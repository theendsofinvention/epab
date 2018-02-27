# coding=utf-8
"""
Handles EPAB's config file
"""

import sys
from pathlib import Path

import yaml

TEST_VALUES = {
    'package': 'test',
}


class _ConfigProp:

    def __init__(self, default=None, mandatory=False, cast=None):
        if default and mandatory:
            raise RuntimeError('Config option can\'t have a default and be mandatory at the same time')
        self.default = default
        self.mandatory = mandatory
        self.cast = cast

    # pylint: disable=inconsistent-return-statements
    def __set__(self, instance, value):

        components = self.name.split('__')
        key = components.pop()
        target = getattr(instance, '_data')
        while components:
            com = components.pop(0)
            target = target.get(com)
        target[key] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        components = self.name.split('__')
        value = None
        # pylint: disable=protected-access
        # noinspection PyProtectedMember
        src = instance._data
        while components:
            com = components.pop(0)
            value = src.get(com)
            src = value
            if value is None:
                break
        if self.default is not None and value is None:
            return self.default
        if value is not None and self.cast:
            return self.cast(value)

        return value

    # pylint: disable=attribute-defined-outside-init
    def __set_name__(self, owner, name):
        self.name = name


class _Config:
    def __init__(self):
        self._data = {}

    def load(self, config_file='epab.yml'):
        """
        Loads configuration data from a config file

        Args:
            config_file: file to load the data from (defaults to "epab.yml")
        """
        config_file = Path(config_file).absolute()
        if not config_file.exists():
            if not hasattr(sys, '_called_from_test'):
                raise FileNotFoundError(f'Config file not found: {config_file}')
            self._data = TEST_VALUES
        else:
            with config_file.open() as stream:
                self._data = yaml.safe_load(stream)
        self.check_mandatory_values(self)

    @classmethod
    def check_mandatory_values(cls, instance: '_Config'):
        """
        Makes sure we have all mandatory values declared

        Args:
            instance: config instance

        """
        for key in dir(cls):
            if not key.startswith('_'):
                member = getattr(cls, key)
                if isinstance(member, _ConfigProp):
                    if member.mandatory and getattr(instance, key) is None:
                        nice_name = key.replace('__', '/')
                        raise ValueError(f'Missing config options: {nice_name}')


class Config(_Config):
    """
    Manages configuration for EPAB
    """
    changelog__disable = _ConfigProp(cast=bool)
    changelog__file = _ConfigProp(default='CHANGELOG.rst')
    test__av_runner_options = _ConfigProp(cast=str)
    test__runner_options = _ConfigProp(cast=str)
    test__duration = _ConfigProp(default='10', cast=str)
    test__target = _ConfigProp(default='test', cast=str)
    test__coverage__fail_under = _ConfigProp(cast=int, default=20)
    lint__line_length = _ConfigProp(default='120', cast=str)
    package = _ConfigProp(mandatory=True)
    entry_point = _ConfigProp(cast=str, default='')
    data_files = _ConfigProp(cast=tuple, default=tuple())
    doc__repo = _ConfigProp(cast=str)
    doc__folder = _ConfigProp(default='./doc')
    quiet = _ConfigProp(default=False, cast=bool)
    verbose = _ConfigProp(default=False, cast=bool)
    artifacts = _ConfigProp(cast=list)
    flake8__exclude = _ConfigProp(cast=str, default='')


CONFIG = Config()


if __name__ == '__main__':
    CONFIG.load()
    print(CONFIG.changelog__disable)
    print(CONFIG.test__av_runner_options)
    print(CONFIG.test__runner_options)
    print(CONFIG.lint__line_length)
    print(CONFIG.package)
    print(CONFIG.changelog__file)
    print(CONFIG.artifacts)
    if CONFIG.artifacts:
        assert isinstance(CONFIG.artifacts, list)
        for x in CONFIG.artifacts:
            print(x)
            print(list(Path('.').glob(x)))
