# coding=utf-8
"""
Manages the local Git repo
"""
import logging
import os
import sys
import typing

import git
from git.exc import GitCommandError

from epab.bases.repo import BaseRepo

LOGGER = logging.getLogger('EPAB')


# pylint: disable=too-many-public-methods
class Repo(BaseRepo):
    """
    Wrapper for git.Repo
    """

    def get_current_branch(self) -> str:
        """
        :return: current branch
        :rtype: str
        """
        current_branch: str = self.repo.active_branch.name
        LOGGER.debug('current branch: %s', current_branch)
        return current_branch

    def tag(self, tag: str, overwrite: bool = False) -> None:
        """
        Tags the current commit

        :param tag: tag
        :type tag: str
        :param overwrite: overwrite existing tag
        :type overwrite: bool
        """
        LOGGER.info('tagging repo: %s', tag)
        try:
            self.repo.create_tag(tag)
        except GitCommandError as exc:
            if 'already exists' in exc.stderr and overwrite:
                LOGGER.info('overwriting existing tag')
                self.remove_tag(tag)
                self.repo.create_tag(tag)
            else:
                LOGGER.exception('error while tagging repo')
                raise

    def list_tags(self, pattern: str = None) -> typing.List[str]:
        """
        Returns list of tags, optionally matching "pattern"

        :param pattern: optional pattern to filter results
        :type pattern: str
        :return: existing tags
        :rtype: list of str
        """
        tags: typing.List[str] = [str(tag) for tag in self.repo.tags]
        if not pattern:
            LOGGER.debug('tags found in repo: %s', tags)
            return tags

        LOGGER.debug('filtering tags with pattern: %s', pattern)
        filtered_tags: typing.List[str] = [tag for tag in tags if pattern in tag]
        LOGGER.debug('filtered tags: %s', filtered_tags)
        return filtered_tags

    def remove_tag(self, *tag: str):
        """
        Removes tag(s) from the rpo

        :param tag: tags to remove
        :type tag: tuple
        """
        LOGGER.info('removing tag(s) from repo: %s', tag)

        self.repo.delete_tag(*tag)

    def get_latest_tag(self) -> typing.Optional[str]:
        """
        :return:latest tag on the repo in the form TAG[-DISTANCE+[DIRTY]]
        :rtype: str
        """
        try:
            latest_tag: str = self.repo.git.describe(tags=True, abbrev=0)
            LOGGER.debug('latest tag: %s', latest_tag)
            return latest_tag
        except GitCommandError as exc:
            if 'No names found' in exc.stderr:
                LOGGER.debug('no tag found in repo')
                return None
            raise  # pragma: no cover

    def latest_commit(self) -> git.Commit:
        """
        :return: latest commit
        :rtype: git.Commit object
        """
        latest_commit: git.Commit = self.repo.head.commit
        LOGGER.debug('latest commit: %s', latest_commit)
        return latest_commit

    def is_on_tag(self) -> bool:
        """
        :return: True if latest commit is tagged
        :rtype: bool
        """
        if self.get_current_tag():
            LOGGER.debug('latest commit is tagged')
            return True

        LOGGER.debug('latest commit is NOT tagged')
        return False

    def get_current_tag(self) -> typing.Optional[str]:
        """
        :return: tag name if current commit is on tag, else None
        :rtype: optional str
        """
        tags = list(self.repo.tags)
        if not tags:
            LOGGER.debug('no tag found')
            return None
        for tag in tags:
            LOGGER.debug('tag found: %s; comparing with commit', tag)
            if tag.commit == self.latest_commit():
                tag_name: str = tag.name
                LOGGER.debug('found tag on commit: %s', tag_name)
                return tag_name

        LOGGER.debug('no tag found on latest commit')
        return None

    def stash(self, stash_name: str):
        """
        Stashes the current working tree changes

        :param stash_name: name of the stash
        :type stash_name: str
        """
        if self.stashed:
            LOGGER.error('already stashed')
            sys.exit(-1)
        else:
            if not self.index_is_empty():
                LOGGER.error('cannot stash; index is not empty')
                sys.exit(-1)
            if self.untracked_files():
                LOGGER.error('cannot stash; there are untracked files')
                sys.exit(-1)
            if self.changed_files():
                LOGGER.info('stashing changes')
                self.repo.git.stash('push', '-u', '-k', '-m', f'"{stash_name}"')
                self.stashed = True
            else:
                LOGGER.info('no changes to stash')

    def unstash(self):
        """
        Pops the last stash if EPAB made a stash before
        """
        if not self.stashed:
            LOGGER.error('no stash')
        else:
            LOGGER.info('popping stash')
            self.repo.git.stash('pop')
            self.stashed = False

    @staticmethod
    def ensure():
        """
        Makes sure the current working directory is a Git repository.
        """
        LOGGER.debug('checking repository')
        if not os.path.exists('.git'):
            LOGGER.error('This command is meant to be ran in a Git repository.')
            sys.exit(-1)
        LOGGER.debug('repository OK')

    def last_commit_msg(self) -> str:
        """
        :return: last commit message
        :rtype: str
        """
        last_msg: str = self.latest_commit().message.rstrip()
        LOGGER.debug('last msg: %s', last_msg)
        return last_msg

    def untracked_files(self) -> typing.List[str]:
        """
        :return: of untracked files
        :rtype: list
        """
        untracked_files = list(self.repo.untracked_files)
        LOGGER.debug('untracked files: %s', untracked_files)
        return untracked_files

    def status(self) -> str:
        """
        :return: Git status
        :rtype: str
        """
        status: str = self.repo.git.status()
        LOGGER.debug('git status: %s', status)
        return status

    def list_staged_files(self) -> typing.List[str]:
        """
        :return: staged files
        :rtype: list of str
        """
        staged_files: typing.List[str] = [x.a_path for x in self.repo.index.diff('HEAD')]
        LOGGER.debug('staged files: %s', staged_files)
        return staged_files

    def index_is_empty(self) -> bool:
        """
        :return: True if index is empty (no staged changes)
        :rtype: bool
        """
        index_empty: bool = len(self.repo.index.diff(self.repo.head.commit)) == 0
        LOGGER.debug('index is empty: %s', index_empty)
        return index_empty

    def changed_files(self) -> typing.List[str]:
        """
        :return: changed files
        :rtype: list of str
        """
        changed_files: typing.List[str] = [x.a_path for x in self.repo.index.diff(None)]
        LOGGER.debug('changed files: %s', changed_files)
        return changed_files

    def reset_index(self):
        """
        Resets changes in the index (working tree untouched)
        """
        LOGGER.warning('resetting changes')
        self.repo.index.reset()

    def stage_all(self):
        """
        Stages all changed and untracked files
        """
        LOGGER.info('Staging all files')
        self.repo.git.add(A=True)

    def stage_modified(self):
        """
        Stages modified files only (no untracked)
        """
        LOGGER.info('Staging modified files')
        self.repo.git.add(u=True)

    def stage_subset(self, *files_to_add: str):
        """
        Stages a subset of files

        :param files_to_add: files to stage
        :type files_to_add: str
        """
        LOGGER.info('staging files: %s', files_to_add)
        self.repo.git.add(*files_to_add, A=True)

    @staticmethod
    def add_skip_ci_to_commit_msg(message: str) -> str:
        """
        Adds a "[skip ci]" tag at the end of a (possibly multi-line) commit message

        :param message: commit message
        :type message: str
        :return: edited commit message
        :rtype: str
        """
        first_line_index = message.find('\n')
        if first_line_index == -1:
            edited_message = message + ' [skip ci]'
        else:
            edited_message = message[:first_line_index] + ' [skip ci]' + message[first_line_index:]
        LOGGER.debug('edited commit message: %s', edited_message)
        return edited_message

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

        :param message: first line of the message
        :type message: str
        :param files_to_add: files to commit
        :type files_to_add: optional list of str
        :param allow_empty: allow dummy commit
        :type allow_empty: bool
        """
        message = str(message)
        LOGGER.debug('message: %s', message)

        files_to_add = self._sanitize_files_to_add(files_to_add)
        LOGGER.debug('files to add: %s', files_to_add)

        if not message:
            LOGGER.error('empty commit message')
            sys.exit(-1)

        if os.getenv('APPVEYOR'):
            LOGGER.info('committing on AV, adding skip_ci tag')
            message = self.add_skip_ci_to_commit_msg(message)

        if files_to_add is None:
            self.stage_all()
        else:
            self.reset_index()
            self.stage_subset(*files_to_add)

        if self.index_is_empty() and not allow_empty:
            LOGGER.error('empty commit')
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
            LOGGER.error('missing either "new_message" or "append_to_msg"')
            sys.exit(-1)
        return message

    def amend_commit(
            self,
            append_to_msg: typing.Optional[str] = None,
            new_message: typing.Optional[str] = None,
            files_to_add: typing.Optional[typing.Union[typing.List[str], str]] = None,
    ):
        """
        Amends last commit with either an entirely new commit message, or an edited version of the previous one

        Note: it is an error to provide both "append_to_msg" and "new_message"

        :param append_to_msg: message to append to previous commit message
        :type append_to_msg: str
        :param new_message: new commit message
        :type new_message: str
        :param files_to_add: optional list of files to add to this commit
        :type files_to_add: str or list of str
        """

        if new_message and append_to_msg:
            LOGGER.error('Cannot use "new_message" and "append_to_msg" together')
            sys.exit(-1)

        files_to_add = self._sanitize_files_to_add(files_to_add)

        message = self._sanitize_amend_commit_message(append_to_msg, new_message)

        if os.getenv('APPVEYOR'):
            message = f'{message} [skip ci]'

        LOGGER.info('amending commit with new message: %s', message)
        latest_tag = self.get_current_tag()

        if latest_tag:
            LOGGER.info('removing tag: %s', latest_tag)
            self.remove_tag(latest_tag)

        LOGGER.info('going back one commit')
        branch = self.repo.head.reference
        try:
            branch.commit = self.repo.head.commit.parents[0]
        except IndexError:
            LOGGER.error('cannot amend the first commit')
            sys.exit(-1)
        if files_to_add:
            self.stage_subset(*files_to_add)
        else:
            self.stage_all()
        self.repo.index.commit(message, skip_hooks=True)
        if latest_tag:
            LOGGER.info('resetting tag: %s', latest_tag)
            self.tag(latest_tag)

    def merge(self, ref_name: str):
        """
        Merges two refs

        Args:
            ref_name: ref to merge in the current one
        """
        if self.is_dirty():
            LOGGER.error('repository is dirty; cannot merge: %s', ref_name)
            sys.exit(-1)
        LOGGER.info('merging ref: "%s" into branch: %s', ref_name, self.get_current_branch())
        self.repo.git.merge(ref_name)

    def push(self, set_upstream: bool = True):
        """
        Pushes all refs (branches and tags) to origin
        """
        LOGGER.info('pushing repo to origin')

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
        LOGGER.info('pushing tags to origin')

        self.repo.git.push('--tags')

    def list_branches(self) -> typing.List[str]:
        """
        :return: branches names
        :rtype: list of str
        """
        branches: typing.List[str] = [head.name for head in self.repo.heads]
        LOGGER.debug('branches: %s', branches)
        return branches

    def get_sha(self) -> str:
        """
        :return: SHA of the latest commit
        :rtype: str
        """
        current_sha: str = self.repo.head.commit.hexsha
        LOGGER.debug('current commit SHA: %s', current_sha)
        return current_sha

    def get_short_sha(self) -> str:
        """
        :return: short SHA of the latest commit
        :rtype: str
        """
        short_sha: str = self.get_sha()[:7]
        LOGGER.debug('short SHA: %s', short_sha)
        return short_sha

    def _validate_branch_name(self, branch_name: str):
        try:
            self.repo.git.check_ref_format('--branch', branch_name)
        except git.exc.GitCommandError:  # pylint: disable=no-member
            LOGGER.error('invalid branch name: %s', branch_name)
            sys.exit(-1)

    def checkout(self, reference: str):
        """
        Checks out a reference.

        If the index is dirty, or if the repository contains untracked files, the function will fail.

        :param reference: reference to check out
        :type reference: str
        """
        LOGGER.info('checking out: %s', reference)
        if not self.index_is_empty():
            LOGGER.error('index contains change; cannot checkout. Status:\n %s', self.status())
            sys.exit(-1)
        if self.is_dirty(untracked=True):
            LOGGER.error('repository is dirty; cannot checkout "%s"', reference)
            LOGGER.error('repository is dirty; cannot checkout. Status:\n %s', self.status())
            sys.exit(-1)

        LOGGER.debug('going through all present references')
        for head in self.repo.heads:
            if head.name == reference:
                LOGGER.debug('resetting repo index and working tree to: %s', reference)
                self.repo.head.reference = head
                self.repo.head.reset(index=True, working_tree=True)
                break
        else:
            LOGGER.error('reference not found: %s', reference)
            sys.exit(-1)

    def create_branch(self, branch_name: str):
        """
        Creates a new branch

        Args:
            branch_name: name of the branch

        """
        LOGGER.info('creating branch: %s', branch_name)
        self._validate_branch_name(branch_name)
        if branch_name in self.list_branches():
            LOGGER.error('branch already exists')
            sys.exit(-1)
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
            LOGGER.error('index is not empty')
            result = True
        changed_files = self.changed_files()
        if bool(changed_files):

            LOGGER.error(f'Repo has %s modified files: %s', len(changed_files), changed_files)
            result = True
        if untracked:
            result = result or bool(self.untracked_files())
        return result
