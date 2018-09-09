# coding=utf-8
"""
Base class for a Repo object
"""
import typing
from abc import ABCMeta, abstractmethod

import git


# pylint: disable=too-many-public-methods
class BaseRepo(metaclass=ABCMeta):
    """
    Base class for a Repo object
    """

    def __init__(self):
        self.stashed = False
        self.repo = git.Repo()

    @abstractmethod
    def get_current_branch(self):
        """
        Returns: current branch as a string
        """
        pass

    @abstractmethod
    def tag(self, tag, overwrite):
        """
        Tags the repo

        Args:
            tag: tag as a string
            overwrite: replace existing tag
        """
        pass

    @abstractmethod
    def list_tags(self, pattern):
        """
        Returns list of tags, optionally matching "pattern"

        Args:
            pattern: optional pattern to match

        Returns: list of strings
        """
        pass

    @abstractmethod
    def remove_tag(self, *tag: str):
        """
        Deletes a tag from the repo

        Args:
            tag: tag to remove
        """
        pass

    @abstractmethod
    def get_latest_tag(self):
        """
        Returns: latest tag on the repo in the form TAG[-DISTANCE+[DIRTY]]
        """
        pass

    @abstractmethod
    def latest_commit(self):
        """

        Returns: latest commit

        """
        pass

    @abstractmethod
    def get_current_tag(self):
        """
        :return: tag name if current commit is on tag, else None
        """
        pass

    @abstractmethod
    def is_on_tag(self):
        """
        :return: True if latest commit is tagged
        """
        pass

    @abstractmethod
    def stash(self, stash_name):
        """
        Creates a stash

        Args:
            stash_name: name of the stash for easier later referencing
        """
        pass

    @abstractmethod
    def unstash(self):
        """
        Pops the last stash if EPAB made a stash before
        """
        pass

    @staticmethod
    @abstractmethod
    def ensure():
        """
        Makes sure the current working directory is a Git repository.
        """
        pass

    @abstractmethod
    def last_commit_msg(self):
        """
        Returns: latest commit comment
        """
        pass

    @abstractmethod
    def untracked_files(self):
        """

        Returns: list of untracked files

        """
        pass

    @abstractmethod
    def status(self):
        """

        Returns: Git status

        """
        pass

    @abstractmethod
    def list_staged_files(self):
        """

        Returns: list of staged files

        """
        pass

    @abstractmethod
    def index_is_empty(self):
        """

        Returns: True if index is empty (no staged changes)

        """
        pass

    @abstractmethod
    def changed_files(self):
        """

        Returns: list of changed files

        """
        pass

    @abstractmethod
    def reset_index(self):
        """
        Resets changes in the index (working tree untouched)
        """
        pass

    @abstractmethod
    def stage_all(self):
        """
        Stages all changed and untracked files
        """
        pass

    @abstractmethod
    def stage_modified(self):
        """
        Stages modified files only (no untracked)
        """
        pass

    @abstractmethod
    def stage_subset(self, *files_to_add: str):
        """
        Stages a subset of files
        Args:
            *files_to_add: files to stage
        """
        pass

    @staticmethod
    @abstractmethod
    def add_skip_ci_to_commit_msg(message):
        """
        Adds a "[skip ci]" tag at the end of a (possibly multi-line) commit message

        :param message: commit message
        :type message: str
        :return: edited commit message
        :rtype: str
        """

    @staticmethod
    @abstractmethod
    def _sanitize_files_to_add(files_to_add):
        pass

    @abstractmethod
    def commit(self, message, files_to_add, allow_empty):
        """
        Commits changes to the repo

        Args:
            message: first line of the message
            files_to_add: optional list of files to commit
            allow_empty: allow dummy commit
        """
        pass

    @abstractmethod
    def _sanitize_amend_commit_message(self, append_to_msg, new_message, previous_message):
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def merge(self, ref_name):
        """
        Merges two refs

        Args:
            ref_name: ref to merge in the current one
        """
        pass

    @abstractmethod
    def push(self, set_upstream: bool = True):
        """
        Pushes all refs (branches and tags) to origin
        """
        pass

    @abstractmethod
    def push_tags(self):
        """
        Pushes tags to origin
        """
        pass

    @abstractmethod
    def list_branches(self):
        """
        Returns: branches names as a list of string
        """
        pass

    @abstractmethod
    def get_sha(self):
        """
        Returns: SHA of the latest commit
        """
        pass

    @abstractmethod
    def get_short_sha(self):
        """
        Returns: short SHA of the latest commit
        """
        pass

    @abstractmethod
    def _validate_branch_name(self, branch_name):
        pass

    @abstractmethod
    def checkout(self, reference):
        """
        Checks out a reference.

        If the index is dirty, or if the repository contains untracked files, the function will fail.

        Args:
            reference: reference to check out as a string

        """
        pass

    @abstractmethod
    def create_branch(self, branch_name):
        """
        Creates a new branch

        Args:
            branch_name: name of the branch

        """
        pass

    @abstractmethod
    def create_branch_and_checkout(self, branch_name):
        """
        Creates a new branch if it doesn't exist

        Args:
            branch_name: branch name
        """
        pass

    @abstractmethod
    def is_dirty(self, untracked):
        """
        Checks if the current repository contains uncommitted or untracked changes

        Returns: true if the repository is clean
        """
        pass
