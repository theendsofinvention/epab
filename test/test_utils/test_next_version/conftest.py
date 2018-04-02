# coding=utf-8

import time
import typing
from pathlib import Path

import pytest

import epab.utils
from epab.core import CTX

UML_DIR = Path('./test/uml').absolute()
UML_DIR.mkdir(exist_ok=True)


class Repo(epab.utils.Repo):

    def __init__(self):
        epab.utils.Repo.__init__(self)
        self.uml = ['@startuml']

    def commit(
            self,
            message: str,
            files_to_add: typing.Optional[typing.Union[typing.List[str], str]] = None,
            allow_empty: bool = False,
    ):
        super(Repo, self).commit(message, files_to_add, allow_empty)
        self.uml.append(f'{self.get_current_branch()} -> {self.get_current_branch()}: commit')

    def merge(self, ref_name: str):
        super(Repo, self).merge(ref_name)
        self.uml.append(f'{ref_name} ->o {self.get_current_branch()}: merge')

    def checkout(self, reference):
        init_branch = self.get_current_branch()
        super(Repo, self).checkout(reference)
        self.uml.append(f'{init_branch} ->> {reference}: checkout')

    def create_branch_and_checkout(self, branch_name):
        self.create_branch(branch_name)
        self.checkout(branch_name)
        if CTX.appveyor:
            time.sleep(1)
        else:
            time.sleep(0.1)

    def tag(self, tag: str, overwrite: bool = False):
        if tag is None:
            tag = epab.utils.get_next_version()
        branch = self.get_current_branch()
        self.uml.append(f'{branch} --> {branch}: TAG: {tag}')
        # self.uml.append(f'ref over {branch}: {tag}')
        super(Repo, self).tag(tag, overwrite)

    def mark(self, text: str):
        self.uml.append(f'ref over {self.get_current_branch()}: {text}')


# noinspection PyTypeChecker
@pytest.fixture(name='repo')
def _git_repo(request, dummy_git_repo, monkeypatch):
    test_name = request.node.name
    # noinspection SpellCheckingInspection
    uml = [
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
    repo = Repo()
    CTX.repo = repo
    yield repo
    uml.extend(repo.uml)
    # noinspection SpellCheckingInspection
    uml.append('@enduml')
    uml = [x.replace('/', '.') for x in uml]
    # noinspection SpellCheckingInspection
    Path(UML_DIR, test_name + '.puml').write_text('\n'.join(uml))
