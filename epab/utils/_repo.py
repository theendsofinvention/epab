# coding=utf-8
"""
Manages the local Git repo
"""
import os
import sys
import typing

import git
from git.exc import GitCommandError

import epab.utils
from epab.bases.repo import BaseRepo
from epab.core import CTX


# pylint: disable=too-many-public-methods
class Repo(BaseRepo):
    """
    Wrapper for git.Repo
    """

    def get_current_branch(self) -> str:
        """
        Returns: current branch as a string
        """
        return self.repo.active_branch.name

    def tag(self, tag: str, overwrite: bool = False):
        """
        Tags the repo

        Args:
            tag: tag as a string
            overwrite: replace existing tag
        """
        epab.utils.info(f'Tagging repo: {tag}')
        if CTX.dry_run:
            epab.utils.info('Not tagging; DRY RUN')
            return
        try:
            self.repo.create_tag(tag)
        except GitCommandError as exc:
            if 'already exists' in exc.stderr and overwrite:
                self.remove_tag(tag)
                self.repo.create_tag(tag)
            else:
                raise

    def list_tags(self, pattern: str = None) -> typing.List[str]:
        """
        Returns list of tags, optionally matching "pattern"

        Args:
            pattern: optional pattern to match

        Returns: list of strings
        """
        tags = [str(tag) for tag in self.repo.tags]
        if not pattern:
            return tags

        return [tag for tag in tags if pattern in tag]

    def remove_tag(self, *tag: str):
        """
        Deletes a tag from the repo

        Args:
            tag: tag to remove
        """
        epab.utils.info(f'Removing tag: {tag}')
        if CTX.dry_run:
            return
        self.repo.delete_tag(*tag)

    def get_latest_tag(self) -> typing.Optional[str]:
        """
        Returns: latest tag on the repo in the form TAG[-DISTANCE+[DIRTY]]
        """
        try:
            return self.repo.git.describe(tags=True, abbrev=0)
        except GitCommandError as exc:
            if 'No names found' in exc.stderr:
                return None
            raise  # pragma: no cover

    def latest_commit(self) -> git.Commit:
        """

        Returns: latest commit

        """
        return self.repo.head.commit

    def is_on_tag(self) -> bool:
        """
        :return: True if latest commit is tagged
        """
        if self.get_current_tag():
            return True

        return False

    def get_current_tag(self) -> typing.Optional[str]:
        """
        :return: tag name if current commit is on tag, else None
        """
        tags = list(self.repo.tags)
        if not tags:
            return None
        for tag in tags:
            if tag.commit == self.latest_commit():
                return tag.name

        return None

    def stash(self, stash_name: str):
        """
        Creates a stash

        Args:
            stash_name: name of the stash for easier later referencing
        """
        if self.stashed:
            epab.utils.error('Already stashed')
        else:
            if not self.index_is_empty():
                epab.utils.error('Cannot stash; index is not empty')
                sys.exit(-1)
            if self.untracked_files():
                epab.utils.error('Cannot stash; there are untracked files')
                sys.exit(-1)
            if self.changed_files():
                epab.utils.info('Stashing changes')
                self.repo.git.stash('push', '-u', '-k', '-m', f'"{stash_name}"')
                self.stashed = True
            else:
                epab.utils.info('No changes to stash')

    def unstash(self):
        """
        Pops the last stash if EPAB made a stash before
        """
        if not self.stashed:
            epab.utils.error('No stash')
        else:
            epab.utils.info('Popping stash')
            self.repo.git.stash('pop')
            self.stashed = False

    @staticmethod
    def ensure():
        """
        Makes sure the current working directory is a Git repository.
        """
        epab.utils.cmd_start('checking repository')
        if not os.path.exists('.git'):
            if CTX.dry_run:
                epab.utils.cmd_end(' -> DRY RUN')
                return
            epab.utils.cmd_end(' -> ERROR')
            epab.utils.error('This command is meant to be ran in a Git repository.')
            sys.exit(-1)
        epab.utils.cmd_end(' -> OK')

    def last_commit_msg(self) -> str:
        """
        Returns: latest commit comment
        """
        return self.latest_commit().message.rstrip()

    def untracked_files(self) -> typing.List[str]:
        """

        Returns: list of untracked files

        """
        return self.repo.untracked_files

    def status(self):
        """

        Returns: Git status

        """
        return self.repo.git.status()

    def list_staged_files(self) -> typing.List[str]:
        """

        Returns: list of staged files

        """
        return [x.a_path for x in self.repo.index.diff('HEAD')]

    def index_is_empty(self) -> bool:
        """

        Returns: True if index is empty (no staged changes)

        """
        return len(self.repo.index.diff(self.repo.head.commit)) == 0

    def changed_files(self) -> typing.List[str]:
        """

        Returns: list of changed files

        """
        return [x.a_path for x in self.repo.index.diff(None)]

    def reset_index(self):
        """
        Resets changes in the index (working tree untouched)
        """
        epab.utils.info('Resetting changes')
        self.repo.index.reset()

    def stage_all(self):
        """
        Stages all changed and untracked files
        """
        epab.utils.info('Staging all files')
        self.repo.git.add(A=True, n=CTX.dry_run)

    def stage_modified(self):
        """
        Stages modified files only (no untracked)
        """
        epab.utils.info('Staging modified files')
        self.repo.git.add(u=True, n=CTX.dry_run)

    def stage_subset(self, *files_to_add: str):
        """
        Stages a subset of files
        Args:
            *files_to_add: files to stage
        """
        epab.utils.info(f'Staging files: {files_to_add}')
        self.repo.git.add(*files_to_add, A=True, n=CTX.dry_run)
        # self.repo.index.add(files_to_add)

    @staticmethod
    def _add_skip_ci_to_commit_msg(message: str):
        first_line_index = message.find('\n')
        if first_line_index == -1:
            return message + ' [skip ci]'
        return message[:first_line_index] + ' [skip ci]' + message[first_line_index:]

    @staticmethod
    def _sanitize_files_to_add(
            files_to_add: typing.Optional[typing.Union[typing.List[str], str]] = None
    ) -> typing.Optional[typing.List[str]]:

        if not files_to_add:
            return None

        if isinstance(files_to_add, str):
            return [files_to_add]

        return files_to_add

    def commit(
            self,
            message: str,
            files_to_add: typing.Optional[typing.Union[typing.List[str], str]] = None,
            allow_empty: bool = False,
    ):
        """
        Commits changes to the repo

        Args:
            message: first line of the message
            files_to_add: optional list of files to commit
            allow_empty: allow dummy commit
        """

        files_to_add = self._sanitize_files_to_add(files_to_add)
        message = str(message)

        if not message:
            epab.utils.error('Empty commit message')
            sys.exit(1)

        if os.getenv('APPVEYOR'):
            message = self._add_skip_ci_to_commit_msg(message)

            epab.utils.info(f'Committing with message: {message}')

        if CTX.dry_run:
            return

        if files_to_add is None:
            self.stage_all()
        else:
            self.reset_index()
            self.stage_subset(*files_to_add)

        if self.index_is_empty() and not allow_empty:
            epab.utils.error('Empty commit')
            sys.exit(-1)

        self.repo.index.commit(message=message)

    def _sanitize_amend_commit_message(
            self,
            append_to_msg: typing.Optional[str] = None,
            new_message: typing.Optional[str] = None,
            previous_message: str = None,
    ) -> str:
        message = None
        if new_message:
            message = new_message
        if append_to_msg:
            last_commit_msg = previous_message or self.repo.head.commit.message
            last_commit_msg = last_commit_msg.rstrip()
            if append_to_msg not in last_commit_msg:
                if '\n\n' not in last_commit_msg:
                    last_commit_msg = f'{last_commit_msg}\n'
                message = '\n'.join((last_commit_msg, append_to_msg))
            else:
                message = last_commit_msg
        if message is None:
            epab.utils.error('Missing either "new_message" or "append_to_msg"')
            sys.exit(-1)
        return message

    def amend_commit(
            self,
            append_to_msg: typing.Optional[str] = None,
            new_message: typing.Optional[str] = None,
            files_to_add: typing.Optional[typing.Union[typing.List[str], str]] = None,
    ):
        """
        Amends last commit

        Args:
            append_to_msg: string to append to previous message
            new_message: new commit message
            files_to_add: optional list of files to commit
        """

        files_to_add = self._sanitize_files_to_add(files_to_add)

        if new_message and append_to_msg:
            epab.utils.error('Cannot use "new_message" and "append_to_msg" together')
            sys.exit(-1)

        message = self._sanitize_amend_commit_message(append_to_msg, new_message)

        if os.getenv('APPVEYOR'):
            message = f'{message} [skip ci]'

        epab.utils.info(f'Amending commit with new message: {message}')
        latest_tag = self.get_current_tag()
        if CTX.dry_run:
            epab.utils.info('Aborting commit amend: DRY RUN')
            return
        if latest_tag:
            epab.utils.info(f'Removing tag: {latest_tag}')
            self.remove_tag(latest_tag)

        epab.utils.info('Going back one commit')
        branch = self.repo.head.reference
        try:
            branch.commit = self.repo.head.commit.parents[0]
        except IndexError:
            epab.utils.error('Cannot amend the first commit')
            sys.exit(-1)
        if files_to_add:
            self.stage_subset(*files_to_add)
        else:
            self.stage_all()
        self.repo.index.commit(message, skip_hooks=True)
        if latest_tag:
            epab.utils.info(f'Resetting tag: {latest_tag}')
            self.tag(latest_tag)

    def merge(self, ref_name: str):
        """
        Merges two refs

        Args:
            ref_name: ref to merge in the current one
        """
        if self.is_dirty():
            epab.utils.error(f'Repository is dirty; cannot merge "{ref_name}"')
            sys.exit(-1)
        epab.utils.info(f'Merging {ref_name} into {self.get_current_branch()}')
        if CTX.dry_run:
            epab.utils.info('Skipping merge: DRY RUN')
            return
        self.repo.git.merge(ref_name)

    def push(self, set_upstream: bool = True):
        """
        Pushes all refs (branches and tags) to origin
        """
        epab.utils.info('Pushing repo to origin')
        if CTX.dry_run:
            return

        try:
            self.repo.git.push()
        except GitCommandError as error:
            if 'has no upstream branch' in error.stderr and set_upstream:
                self.repo.git.push(f'--set-upstream origin {self.get_current_branch()}')
            else:
                raise
        self.push_tags()

    def push_tags(self):
        """
        Pushes tags to origin
        """
        epab.utils.info('Pushing tags to origin')
        if CTX.dry_run:  # pragma: no cover
            return

        self.repo.git.push('--tags')

    def list_branches(self) -> typing.List[str]:
        """
        Returns: branches names as a list of string
        """
        return [head.name for head in self.repo.heads]

    def get_sha(self) -> str:
        """
        Returns: SHA of the latest commit
        """
        return self.repo.head.commit.hexsha

    def get_short_sha(self) -> str:
        """
        Returns: short SHA of the latest commit
        """
        return self.get_sha()[:7]

    def _validate_branch_name(self, branch_name: str):
        try:
            self.repo.git.check_ref_format('--branch', branch_name)
        except git.exc.GitCommandError:  # pylint: disable=no-member
            epab.utils.error(f'Invalid branch name: {branch_name}')
            sys.exit(1)

    def checkout(self, reference: str):
        """
        Checks out a reference.

        If the index is dirty, or if the repository contains untracked files, the function will fail.

        Args:
            reference: reference to check out as a string

        """
        if not self.index_is_empty():
            epab.utils.error('Index contains change; cannot checkout')
            print(self.status())
            sys.exit(-1)
        if self.is_dirty(untracked=True):
            epab.utils.error(f'Repository is dirty; cannot checkout "{reference}"')
            print(self.status())
            sys.exit(-1)
        if CTX.dry_run:
            epab.utils.info('DRY RUN: aborting checkout')
            return
        epab.utils.info(f'Checking out: {reference}')
        for head in self.repo.heads:
            if head.name == reference:
                self.repo.head.reference = head
                self.repo.head.reset(index=True, working_tree=True)
                break
        else:
            epab.utils.error(f'Unknown reference: {reference}')
            sys.exit(-1)

    def create_branch(self, branch_name: str):
        """
        Creates a new branch

        Args:
            branch_name: name of the branch

        """
        epab.utils.info(f'Creating branch: {branch_name}')
        self._validate_branch_name(branch_name)
        if branch_name in self.list_branches():
            epab.utils.error('Branch already exists')
            sys.exit(1)
        new_branch = self.repo.create_head(branch_name)
        new_branch.commit = self.repo.head.commit

    def create_branch_and_checkout(self, branch_name: str):
        """
        Creates a new branch if it doesn't exist

        Args:
            branch_name: branch name
        """
        self.create_branch(branch_name)
        self.checkout(branch_name)

    def is_dirty(self, untracked=False) -> bool:
        """
        Checks if the current repository contains uncommitted or untracked changes

        Returns: true if the repository is clean
        """
        result = False
        if not self.index_is_empty():
            epab.utils.error('Index is not empty')
            result = True
        changed_files = self.changed_files()
        if bool(changed_files):
            epab.utils.error(f'Repo has {len(changed_files)} modified files: {changed_files}')
            result = True
        if untracked:
            result = result or bool(self.untracked_files())
        if CTX.dry_run and result:
            epab.utils.info('Repo was dirty; DRY RUN')
            return False
        return result
