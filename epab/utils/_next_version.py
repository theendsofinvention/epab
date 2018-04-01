# coding=utf-8
"""
Computes next version
"""
import datetime
import re
import typing

import epab.utils
from epab.core import CTX


class Tag:
    """
    Represents a basic version tag
    """
    _re_tag = re.compile(r'(?P<calver>\d+\.\d+\.\d+)'
                         r'\.'
                         r'(?P<quantifier>\d+)'
                         r'(?P<alpha>.*)?')

    _re_alpha = re.compile(r'a(?P<quantifier>\d+)\+(?P<branch>.+)')

    def __init__(self, tag_str: str):
        self._tag_str = tag_str
        self._tag = self._re_tag.match(self._tag_str)
        self._validate_tag_str()
        if self._tag.group('alpha'):
            self._alpha_str = self._tag.group('alpha')
            self._is_alpha = True
            self._alpha = self._re_alpha.match(self._alpha_str)
            self._validate_alpha_str()
        else:
            self._alpha_str = ''
            self._is_alpha = False

    def _validate_tag_str(self):
        if not self._tag:
            raise ValueError(f'Wrong value for tag string: {self._tag_str}')

    def _validate_alpha_str(self):
        if not self._alpha:
            raise ValueError(f'Wrong value for alpha string: {self._alpha_str}')

    @property
    def calver(self) -> str:
        """
        Returns: calver part of the tag
        """
        return self._tag.group('calver')

    @property
    def quantifier(self) -> int:
        """
        Returns: iteration of this calver (number of releases during that day
        """
        return int(self._tag.group('quantifier'))

    @property
    def branch(self):
        """
        Returns: (only for alpha) branch name
        """
        if not self.is_alpha:
            return ''
        return self._alpha.group('branch')

    @property
    def alpha_quantifier(self) -> int:
        """
        Returns: (only for alpha) iteration of the alpha
        """
        if not self.is_alpha:
            return 0
        return int(self._alpha.group('quantifier'))

    @property
    def is_alpha(self) -> bool:
        """
        Returns: True if this tag is an alpha version
        """
        return self._is_alpha

    def __repr__(self):
        return f'Tag({self._tag_str})'

    def __str__(self):
        return self._tag_str


def _get_datetime() -> datetime.datetime:  # pragma: no cover
    return datetime.datetime.utcnow()


def _get_calver() -> str:
    now = _get_datetime()
    return f'{now.year}.{now.month}.{now.day}'


def _next_stable_version(calver: str, list_of_tags: typing.List[Tag]) -> str:
    next_version_quantifier = 1
    if list_of_tags:
        for tag in list_of_tags:
            if tag.is_alpha:
                continue
            next_version_quantifier = max(next_version_quantifier, tag.quantifier + 1)
        return f'{calver}.{next_version_quantifier}'

    return f'{calver}.1'


def _next_alpha_version(next_stable_version: str, list_of_tags: typing.List[Tag]) -> str:
    next_alpha_version_quantifier = 1
    if list_of_tags:
        for tag in list_of_tags:
            if not tag.is_alpha:
                continue
            if next_stable_version not in str(tag):
                continue
            next_alpha_version_quantifier = max(next_alpha_version_quantifier, tag.alpha_quantifier + 1)
        return f'{next_stable_version}a{next_alpha_version_quantifier}+{CTX.repo.get_current_branch()}'

    return f'{next_stable_version}a1+{CTX.repo.get_current_branch()}'


def _get_current_calver_tags(calver: str) -> typing.List[Tag]:
    return [Tag(tag) for tag in CTX.repo.list_tags(calver)]


def get_next_version() -> str:
    """
    Returns: next version for this Git repository
    """
    epab.utils.info('computing next version')
    should_be_alpha = bool(CTX.repo.get_current_branch() != 'master')
    epab.utils.info(f'alpha: {should_be_alpha}')
    calver = _get_calver()
    epab.utils.info(f'current calver: {calver}')
    calver_tags = _get_current_calver_tags(calver)
    epab.utils.info(f'found {len(calver_tags)} matching tags for this calver')
    next_stable_version = _next_stable_version(calver, calver_tags)
    epab.utils.info(f'next stable version: {next_stable_version}')
    if should_be_alpha:
        return _next_alpha_version(next_stable_version, calver_tags)

    return next_stable_version
