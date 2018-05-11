# coding=utf-8
"""
Handles EPAB's config file
"""

import sys
import inspect
from collections import defaultdict
from pathlib import Path

import yaml

TEST_VALUES = {
    'package': 'test',
}


class _ConfigProp:

    def __init__(self, default=None, mandatory=False, cast=None, help_str=''):
        if default and mandatory:
            raise RuntimeError('Config option can\'t have a default and be mandatory at the same time')
        self.default = default
        self.mandatory = mandatory
        self.cast = cast
        self.help = help_str

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

    @classmethod
    def make_default(cls):

        def _add_attributes(attr_list, padding=''):
            nonlocal default_config
            for _attr in sorted(attr_list, key=lambda x: x.name):
                assert isinstance(_attr, _ConfigProp)
                try:
                    _, _attr_name = _attr.name.split('__')
                except ValueError:
                    _attr_name = _attr.name

                default_config += f'{padding}# {_attr.help}\n{padding}# Type: {_attr.cast}\n'
                default_config += padding
                if not _attr.mandatory and not _attr.default:
                    default_config += '# '
                default_config += f'{_attr_name}:'
                if _attr.default:
                    default_config += f' {_attr.default}'
                default_config += '\n\n'

        attributes = defaultdict(list)
        for attr_name, attr in inspect.getmembers(cls):
            # print(attr_name, attr)
            if isinstance(attr, _ConfigProp):
                try:
                    section, attr_name = attr_name.split('__')
                    attributes[section].append(attr)
                except ValueError:
                    attributes['root'].append(attr)
        default_config = '# EPAB configuration file\n\n'
        _add_attributes(attributes['root'])
        del attributes['root']
        for section in sorted(attributes.keys()):
            for attr in attributes[section]:
                if attr.default or attr.mandatory:
                    break
            else:
                default_config += '#'
            default_config += f'{section}:\n'
            _add_attributes(attributes[section], padding='\t')
        Path('epab.yml').write_text(default_config)


    def load(self, config_file='epab.ymml'):
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
