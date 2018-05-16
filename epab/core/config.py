# coding=utf-8
"""
Handles EPAB's config file
"""

import inspect
import sys
import typing
from collections import defaultdict
from pathlib import Path

import yaml

TEST_VALUES = {
    'package': 'test',
}

CONFIG_FILE_NAME = 'epab.yml'


class _ConfigProp:

    def __init__(self, default=None, mandatory=False, cast=None, help_str=''):
        if default and mandatory:
            raise RuntimeError('Config option can\'t have a default and be mandatory at the same time')
        self.default = default
        self.mandatory = mandatory
        self.cast = cast
        self.help = help_str

    def __set__(self, instance, value):

        components = self.name.split('__')
        key = components.pop()
        target = getattr(instance, '_data')
        while components:
            com = components.pop(0)
            if com not in target:
                target[com] = {}
            target = target[com]
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

    @staticmethod
    def _update_sample_config(sample_config: str, attr_list: list, padding: str = '') -> str:
        for attr in sorted(attr_list, key=lambda _attr: _attr.name):
            try:
                _, attr_name = attr.name.split('__')
            except ValueError:
                attr_name = attr.name

            sample_config += f'{padding}# {attr.help}\n{padding}# Type: {attr.cast}\n'
            sample_config += padding
            if not attr.mandatory and not attr.default:
                sample_config += '# '
            sample_config += f'{attr_name}:'
            if attr.default:
                sample_config += f' {attr.default}'
            sample_config += '\n\n'

        return sample_config

    @classmethod
    def _update_sample_config_from_sections(cls, sample_config: str, attributes: dict) -> str:
        for section in sorted(attributes.keys()):
            for attr in attributes[section]:
                if attr.default or attr.mandatory:
                    break
            else:
                sample_config += '#'
            sample_config += f'{section}:\n'
            cls._update_sample_config(sample_config, attributes[section], padding='\t')

        return sample_config

    @classmethod
    def _gather_attributes(cls) -> dict:
        attributes: typing.DefaultDict = defaultdict(list)
        for attr_name, attr in inspect.getmembers(cls):
            if isinstance(attr, _ConfigProp):
                try:
                    section, attr_name = attr_name.split('__')
                    attributes[section].append(attr)
                except ValueError:
                    attributes['root'].append(attr)
        return attributes

    @classmethod
    def make_default(cls):
        """Creates a sample config file"""
        attributes = cls._gather_attributes()
        sample_config = '# EPAB configuration file\n\n'
        cls._update_sample_config(sample_config, attributes['root'])
        del attributes['root']
        sample_config = cls._update_sample_config_from_sections(sample_config, attributes)
        Path(CONFIG_FILE_NAME).write_text(sample_config)

    def load(self, config_file=CONFIG_FILE_NAME):
        """
        Loads configuration data from a config file

        Args:
            config_file: file to load the data from (defaults to "epab.yml")
        """
        config_file = Path(config_file).absolute()
        if not config_file.exists():
            if not hasattr(sys, '_called_from_test'):
                self.make_default()
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
    changelog__disable = _ConfigProp(cast=bool, help_str='Disable changelog creation')
    changelog__file = _ConfigProp(default='CHANGELOG.rst', help_str='Changelog file name')
    test__av_runner_options = _ConfigProp(default='--long', cast=str, help_str='PyTest runner options on Appveyor')
    test__runner_options = _ConfigProp(default='', cast=str, help_str='PyTest runner options')
    test__duration = _ConfigProp(default='10', cast=str, help_str='Number of slow tests to show')
    test__target = _ConfigProp(default='test', cast=str, help_str='PyTest target')
    coverage__fail_under = _ConfigProp(cast=int, default=20, help_str='Minimal coverage to pass tests')
    lint__line_length = _ConfigProp(default='120', cast=str, help_str='Maximum code line length')
    package = _ConfigProp(mandatory=True, cast=str, help_str='Package name')
    freeze__entry_point = _ConfigProp(cast=str, default='', help_str='Entry point for scripts')
    freeze__data_files = _ConfigProp(cast=tuple, default=tuple(), help_str='Packaging data files')
    doc__repo = _ConfigProp(cast=str, help_str='Documentation repository')
    doc__folder = _ConfigProp(default='./doc', help_str='Documentation folder')
    quiet = _ConfigProp(default=False, cast=bool, help_str='Less output')
    verbose = _ConfigProp(default=False, cast=bool, help_str='More output')
    artifacts = _ConfigProp(cast=list, help_str='List of artifacts for AppVeyor')
    flake8__exclude = _ConfigProp(cast=str, default='', help_str='List of files excluded from flake8 analysis')
    qt__res_src = _ConfigProp(cast=str, default='', help_str='Qt resource file (.qrc) location')
    qt__res_tgt = _ConfigProp(cast=str, default='', help_str='Compiled Qt resource file (.py) target location')
    mypy__args = _ConfigProp(cast=str, default='', help_str='Additional args for mypy linter')


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
