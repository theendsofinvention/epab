# coding=utf-8

import time
from pathlib import Path
from queue import deque

import pytest

import epab.utils
from epab.core import CTX

UML_DIR = Path('./test/uml').absolute()
UML_BRANCH = deque(['master'])
UML_DIR.mkdir(exist_ok=True)
# noinspection SpellCheckingInspection
UML = ['@startuml']

REPO = epab.utils.Repo()


class Repo:

    def __init__(self):
        self.repo = epab.utils.Repo()
        self.uml = ['@startuml']
        self.uml_branch = deque(['master'])

    def get_current_branch(self) -> str:
        return self.repo.get_current_branch()

    def commit(self, message='msg'):
        self.repo.commit(message)
        self.uml.append(f'{self.get_current_branch()} -> {self.get_current_branch()}: commit')

    def short_sha(self):
        return self.repo.get_short_sha()

    def get_latest_tag(self):
        return self.repo.get_latest_tag()

    def merge(self, branch_name: str):
        self.repo.merge(branch_name)
        self.uml.append(f'{branch_name} ->o {self.get_current_branch()}: merge')

    def checkout(self, branch_name):
        init_branch = self.get_current_branch()
        self.repo.checkout(branch_name)
        self.uml.append(f'{init_branch} ->> {branch_name}: checkout')
        self.uml_branch.append(branch_name)

    def create_branch_and_checkout(self, branch_name):
        init_branch = self.get_current_branch()
        self.repo.create_branch_and_checkout(branch_name)
        self.uml.append(f'{init_branch} ->> {branch_name}: checkout')
        if CTX.appveyor:
            time.sleep(1)
        else:
            time.sleep(0.1)

    def tag(self, tag=None):
        if tag is None:
            tag = epab.utils.get_next_version()
        branch = self.get_current_branch()
        self.uml.append(f'{branch} --> {branch}: TAG: {tag}')
        self.uml.append(f'ref over {branch}: {tag}')
        self.repo.tag(tag)

# noinspection PyTypeChecker


@pytest.fixture(autouse=True)
def _git_repo(request, dummy_git_repo, monkeypatch):
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
    try:
        monkeypatch.delenv('TEAMCITY_VERSION')
    except KeyError:
        pass
    dummy_git_repo.create()
    REPO = epab.utils.Repo()
    yield
    # noinspection SpellCheckingInspection
    UML.append('@enduml')
    uml = [x.replace('/', '.') for x in UML]
    # noinspection SpellCheckingInspection
    Path(UML_DIR, test_name + '.puml').write_text('\n'.join(uml))
