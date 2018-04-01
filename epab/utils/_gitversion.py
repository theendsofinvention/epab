# coding=utf-8
"""
Wrapper for the GitVersion executable
"""
import json
import os
import datetime
from pathlib import Path

import epab.utils
from epab.core import CTX

from ._resource_path import resource_path

GIT_VERSION_PATH = resource_path('epab', './vendor/GitVersion_4.0.0-beta0013/gitversion.exe')

# noinspection SpellCheckingInspection
GIT_VERSION_CONFIG = r"""
branches:
  master:
    regex: master
    mode: ContinuousDeployment
    tag: ''
    increment: Patch
    prevent-increment-of-merged-branch-version: true
    track-merge-target: false
    tracks-release-branches: false
    is-release-branch: false
  feature:
    regex: features?[/-]
    mode: ContinuousDeployment
    tag: a+{BranchName}
    increment: Patch
    prevent-increment-of-merged-branch-version: false
    track-merge-target: false
    tracks-release-branches: false
    is-release-branch: false
  pull-request:
    regex: (pull|pull\-requests|pr)[/-]
    mode: ContinuousDeployment
    tag: a+PullRequest
    increment: Patch
    prevent-increment-of-merged-branch-version: false
    tag-number-pattern: '[/-](?<number>\d+)[-/]'
    track-merge-target: false
    tracks-release-branches: false
    is-release-branch: false
"""


class GitVersionProp:
    """
    Descriptor for GitVersionResult properties
    """

    def __get__(self, instance, owner):
        components = self.name.split('_')
        prop_name = ''.join(x.title() for x in components)
        return instance.__dict__['_data'][prop_name]

    # pylint: disable=attribute-defined-outside-init
    def __set_name__(self, owner, name):
        # This is a nifty new feature of 3.6
        self.name = name


# pylint: disable=too-many-public-methods
class GitVersionResult:
    """
    Result of a GitVersion inspection
    """

    sha = GitVersionProp()
    major = GitVersionProp()
    minor = GitVersionProp()
    patch = GitVersionProp()
    pre_release_tag = GitVersionProp()
    pre_release_tag_with_dash = GitVersionProp()
    pre_release_label = GitVersionProp()
    pre_release_number = GitVersionProp()
    build_meta_data = GitVersionProp()
    build_meta_data_padded = GitVersionProp()
    build_meta_data_full = GitVersionProp()
    major_minor_patch = GitVersionProp()
    sem_ver = GitVersionProp()
    full_sem_ver = GitVersionProp()
    informational_version = GitVersionProp()
    legacy_sem_ver = GitVersionProp()
    legacy_sem_ver_padded = GitVersionProp()
    assembly_sem_ver = GitVersionProp()
    assembly_sem_file_ver = GitVersionProp()
    branch_name = GitVersionProp()
    commits_since_version_source = GitVersionProp()
    commits_since_version_source_padded = GitVersionProp()
    commit_date = GitVersionProp()

    def __init__(self, raw_result):
        self._data = json.loads(raw_result)


class _Config:
    def __init__(self):
        self.config_file = Path('./GitVersion.yml').absolute()

    def __enter__(self):
        if os.getenv('APPVEYOR'):
            del os.environ['APPVEYOR']
        self.config_file.write_text(GIT_VERSION_CONFIG)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.config_file.unlink()
        if CTX.appveyor:
            os.environ['APPVEYOR'] = 'True'


def _get_calver() -> str:
    now = datetime.datetime.utcnow()
    return now.strftime('%y.%m.%d.')

def get_git_version_info() -> str:
    """
    Returns: next version for this Git repository
    """
    with _Config():
        raw_result, _ = epab.utils.run(str(GIT_VERSION_PATH.absolute()), mute=True)
        info = GitVersionResult(raw_result)
        calver = _get_calver()
        base_version = f'{calver}.{info.patch}'
        # base_version = info.major_minor_patch
        if info.pre_release_number:
            if info.pre_release_label != 'ci':
                base_version = f'{base_version}{info.pre_release_label}{info.pre_release_number}'
        return base_version


def get_raw_gitversion_info() -> GitVersionResult:
    """
    Returns: raw GitVersionResult
    """
    raw_result, _ = epab.utils.run(str(GIT_VERSION_PATH.absolute()), mute=True)
    return GitVersionResult(raw_result)
