# coding=utf-8

import datetime
import os
import time
import uuid
from pathlib import Path
from queue import deque

import pytest
from setuptools_scm import get_version

import epab.utils
from epab.core import CTX

UML_DIR = Path('./test/uml').absolute()
UML_BRANCH = deque(['master'])
UML_DIR.mkdir(exist_ok=True)
# noinspection SpellCheckingInspection
UML = ['@startuml']


REPO = epab.utils.Repo()


# noinspection PyTypeChecker
@pytest.fixture(autouse=True)
def _git_repo(request, dummy_git_repo):
    global UML, REPO
    test_name = request.node.name
    # noinspection SpellCheckingInspection
    UML = [
        '@startuml',
        f'title {test_name}',
        'skinparam ParticipantPadding 20',
        'skinparam BoxPadding 10',
        'participant master'
    ]
    if os.environ.get('TEAMCITY_VERSION'):
        del os.environ['TEAMCITY_VERSION']
    dummy_git_repo.create()
    REPO = epab.utils.Repo()
    yield
    # noinspection SpellCheckingInspection
    UML.append('@enduml')
    uml = [x.replace('/', '.') for x in UML]
    # noinspection SpellCheckingInspection
    Path(UML_DIR, test_name + '.puml').write_text('\n'.join(uml))


def _branch():
    return REPO.get_current_branch()


def _now():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')


def _commit():
    # noinspection PyTypeChecker
    REPO.commit('msg')
    global UML
    UML.append(f'{_branch()} -> {_branch()}: commit')


def _sha():
    # noinspection PyTypeChecker
    return REPO.get_sha()[:7]


def _git_version():
    version = epab.utils.get_git_version_info()
    global UML
    # noinspection SpellCheckingInspection
    UML.append(f'hnote over {_branch()}: GitVersion: {version}')
    return version


def _scm_version(version, dev: int = None, dirty: bool = False) -> str:
    global UML
    if dev is None:
        if dirty:
            version = f'{version}+d{_now()}'
    else:
        if dirty:
            version = f'{version}.dev{dev}+g{_sha()}.d{_now()}'
        else:
            version = f'{version}.dev{dev}+g{_sha()}'
    # noinspection SpellCheckingInspection
    UML.append(f'hnote over {_branch()}: SCM version: {version}')
    return version


def _dirty(untracked=False):
    # noinspection PyTypeChecker
    return REPO.is_dirty(untracked)


def _change(commit=True, tag_before=None, tag_after=None):
    global UML
    if tag_before:
        _tag(tag_before)
    Path('./init').write_text(str(uuid.uuid4()))
    UML.append(f'{_branch()} --> {_branch()}: change')
    if commit:
        _commit()
    if tag_after:
        if tag_after is True:
            _tag()
        else:
            _tag(tag_after)


# noinspection PyTypeChecker
def _tag(tag=None):
    global UML
    if tag is None:
        tag = epab.utils.get_git_version_info()
    UML.append(f'{_branch()} --> {_branch()}: TAG: {tag}')
    UML.append(f'ref over {_branch()}: {tag}')
    REPO.tag(tag)


def _create_branch(branch_name):
    global UML, UML_BRANCH
    init_branch = _branch()
    # noinspection PyTypeChecker
    REPO.create_branch_and_checkout(branch_name)
    UML.append(f'{init_branch} ->> {branch_name}: checkout')
    if CTX.appveyor:
        time.sleep(1)
    else:
        time.sleep(0.1)


def _checkout(branch_name):
    global UML_BRANCH, UML
    init_branch = _branch()
    # noinspection PyTypeChecker
    REPO.checkout(branch_name)
    UML.append(f'{init_branch} ->> {branch_name}: checkout')
    UML_BRANCH.append(branch_name)


def _merge(branch_name):
    global UML, UML_BRANCH
    # noinspection PyTypeChecker
    REPO.merge(branch_name)
    UML.append(f'{branch_name} ->o {_branch()}: merge')


def _latest_tag():
    return REPO.get_latest_tag()


def test_init():
    assert _git_version() == '0.1.0'


def test_get_version():
    _tag('0.1.0')
    assert get_version() == _scm_version('0.1.0')
    _change(commit=False)
    assert get_version() == _scm_version('0.1.1', dev=0, dirty=True)
    _commit()
    assert get_version() == _scm_version('0.1.1', dev=1)
    _change(commit=False)
    assert get_version() == _scm_version('0.1.1', dev=1, dirty=True)


@pytest.mark.long
def test_master():
    assert _git_version() == '0.1.0'
    _tag('0.1.0')
    assert get_version() == _scm_version('0.1.0')
    assert _latest_tag() == '0.1.0'
    _change()
    assert _git_version() == '0.1.1'
    assert get_version() == _scm_version('0.1.1', dev=1)
    _change(commit=False)
    assert _git_version() == '0.1.1'
    assert get_version() == _scm_version('0.1.1', dev=1, dirty=True)
    _commit()
    _tag(_git_version())
    assert _git_version() == '0.1.1'
    assert get_version() == _scm_version('0.1.1')


@pytest.mark.long
@pytest.mark.skip
def test_develop():
    assert _git_version() == '0.1.0'
    _tag('0.1.0')
    _create_branch('develop')
    assert get_version() == _scm_version('0.1.0')
    assert _latest_tag() == '0.1.0'
    _change()
    assert _git_version() == '0.1.1b1'
    assert get_version() == _scm_version('0.1.1', dev=1)
    _tag()
    assert get_version() == _scm_version('0.1.1b1')
    _change(commit=False)
    assert _git_version() == '0.1.1b1'
    assert get_version() == _scm_version('0.1.1b2', dev=0, dirty=True)
    _commit()
    assert _git_version() == '0.1.1b2'
    assert get_version() == _scm_version('0.1.1b2', dev=1)


@pytest.mark.long
def test_feature():
    assert _git_version() == '0.1.0'
    _tag('0.1.0')
    _create_branch('feature/test')
    assert get_version() == _scm_version('0.1.0')
    assert _latest_tag() == '0.1.0'
    _change()
    assert _git_version() == '0.1.1a+test1'
    assert get_version() == _scm_version('0.1.1', dev=1)
    _tag()
    assert _git_version() == '0.1.1a+test1'
    assert get_version() == _scm_version('0.1.1a0')
    _change(commit=False)
    assert _git_version() == '0.1.1a+test1'
    assert get_version() == _scm_version('0.1.1a1', dev=0, dirty=True)
    _commit()
    assert _git_version() == '0.1.1a+test2'
    assert get_version() == _scm_version('0.1.1a1', dev=1)


@pytest.mark.long
def test_pull_request():
    assert _git_version() == '0.1.0'
    _tag('0.1.0')
    _create_branch('pr/1')
    assert get_version() == _scm_version('0.1.0')
    assert _latest_tag() == '0.1.0'
    _change()
    assert _git_version() == '0.1.1a+PullRequest1'
    assert get_version() == _scm_version('0.1.1', dev=1)
    _tag()
    assert _git_version() == '0.1.1a+PullRequest1'
    assert get_version() == _scm_version('0.1.1a0')
    _change(commit=False)
    assert _git_version() == '0.1.1a+PullRequest1'
    assert get_version() == _scm_version('0.1.1a1', dev=0, dirty=True)
    _commit()
    assert _git_version() == '0.1.1a+PullRequest2'
    assert get_version() == _scm_version('0.1.1a1', dev=1)


@pytest.mark.long
@pytest.mark.skip
def test_release():
    assert _git_version() == '0.1.0'
    _tag('0.1.0')
    _create_branch('release/test')
    assert get_version() == _scm_version('0.1.0')
    assert _latest_tag() == '0.1.0'
    _change()
    assert _git_version() == '0.1.1rc1'
    assert get_version() == _scm_version('0.1.1', dev=1)
    _tag()
    assert _git_version() == '0.1.1rc1'
    assert get_version() == _scm_version('0.1.1rc1')
    _change(commit=False)
    assert _git_version() == '0.1.1rc1'
    assert get_version() == _scm_version('0.1.1rc2', dev=0, dirty=True)
    _commit()
    assert _git_version() == '0.1.1rc2'
    assert get_version() == _scm_version('0.1.1rc2', dev=1)
    _create_branch('release/0.2.0')
    assert _git_version() == '0.2.0'
    assert get_version() == _scm_version('0.1.1rc2', dev=1)
    _tag()
    assert _git_version() == '0.2.0'
    assert get_version() == _scm_version('0.2.0')


@pytest.mark.long
@pytest.mark.skip
def test_flow():
    assert _git_version() == '0.1.0'
    _tag('0.1.0')
    assert get_version() == _scm_version('0.1.0')
    assert _latest_tag() == '0.1.0'
    _create_branch('develop')
    _change()
    assert _git_version() == '0.1.1b1'
    assert get_version() == _scm_version('0.1.1', dev=1)
    _checkout('master')
    assert _git_version() == '0.1.0'
    assert get_version() == _scm_version('0.1.0')
    _checkout('develop')
    assert _git_version() == '0.1.1b1'
    _tag()
    assert get_version() == _scm_version('0.1.1b1')
    _change()
    assert _git_version() == '0.1.1b2'
    assert get_version() == _scm_version('0.1.1b2', dev=1)
    _change(commit=False)
    assert _git_version() == '0.1.1b2'
    assert get_version() == _scm_version('0.1.1b2', dev=1, dirty=True)
    _commit()
    assert _git_version() == '0.1.1b3'
    assert get_version() == _scm_version('0.1.1b2', dev=2)
    _checkout('master')
    _merge('develop')
    assert _git_version() == '0.1.1'
    assert get_version() == _scm_version('0.1.1b2', dev=2)
    _tag()
    assert _git_version() == '0.1.1'
    assert get_version() == _scm_version('0.1.1')


@pytest.mark.long
@pytest.mark.skip
def test_flow_release():
    _tag('0.1.0')
    _create_branch('develop')
    for _ in range(10):
        _change()
    assert _git_version() == '0.1.1b10'
    assert get_version() == _scm_version('0.1.1', dev=10)
    _create_branch('release/0.1.1')
    assert _git_version() == '0.1.1rc10'
    assert get_version() == _scm_version('0.1.1', dev=10)
    _change(tag_after=True)
    assert _git_version() == '0.1.1rc11'
    assert get_version() == _scm_version('0.1.1rc11')
    _checkout('develop')
    _merge('release/0.1.1')
    assert _git_version() == '0.1.1b11'
    assert get_version() == _scm_version('0.1.1rc11')
    _checkout('master')
    _merge('release/0.1.1')
    assert _git_version() == '0.1.1'
    assert get_version() == _scm_version('0.1.1rc11')
    _tag()
    assert _git_version() == '0.1.1'
    assert get_version() == _scm_version('0.1.1')
    _checkout('develop')
    assert _git_version() == '0.1.1'
    assert get_version() == _scm_version('0.1.1')
    _change()
    assert _git_version() == '0.1.2b1'
    assert get_version() == _scm_version('0.1.2', dev=1)


@pytest.mark.long
def test_av_config():
    os.environ['APPVEYOR'] = 'True'
    assert _git_version() == '0.1.0'
    assert not os.getenv('APPVEYOR')
    CTX.appveyor = True
    os.environ['APPVEYOR'] = 'True'
    assert _git_version() == '0.1.0'
    assert os.getenv('APPVEYOR') == 'True'
