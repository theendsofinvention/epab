# coding=utf-8
"""
Updates the changelog with the latest commits
"""

import contextlib
import logging
import re
from pathlib import Path

import click
import elib_run

import epab.utils
from epab.core import CTX, config

LOGGER = logging.getLogger('EPAB')

BOGUS_LINE_PATTERN = re.compile('^(- .*)(\n){2}', flags=re.MULTILINE)

GITCHANGELOG_CONFIG = r"""
output_engine = mustache("markdown")
body_process = ReSub(r'((^|\n)[A-Z]\w+(-\w+)*: .*(\n\s+.*)*)+$', r'') | strip
tag_filter_regexp = r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$'
include_merge = False
ignore_regexps = [
    r'@minor', r'!minor',
    r'@cosmetic', r'!cosmetic',
    r'@refactor', r'!refactor',
    r'@wip', r'!wip',
    r'^([cC]hg|[fF]ix|[nN]ew)\s*:\s*[p|P]kg:',
    r'^([cC]hg|[fF]ix|[nN]ew)\s*:\s*[d|D]ev:',
    r'^(.{3,3}\s*:)?\s*[fF]irst commit.?\s*$',
    r'^release .*$',
    r'^$',  ## ignore commits with empty messages
]
"""


@contextlib.contextmanager
def gitchangelog_config():
    """
    Temporarily installs GitChangelog config
    """
    Path('.gitchangelog.rc').write_text(GITCHANGELOG_CONFIG)
    try:
        yield
    finally:
        Path('.gitchangelog.rc').unlink()


@contextlib.contextmanager
def temporary_tag(tag):
    """
    Temporarily tags the repo
    """
    if tag:
        CTX.repo.tag(tag)
    try:
        yield
    finally:
        if tag:
            CTX.repo.remove_tag(tag)


@epab.utils.run_once
@epab.utils.stashed
@epab.utils.timeit
def _chglog(amend: bool = False, stage: bool = False, next_version: str = None, auto_next_version: bool = False):
    """
    Writes the changelog

    Args:
        amend: amend last commit with changes
        stage: stage changes
    """
    if config.CHANGELOG_DISABLE():
        LOGGER.info('skipping changelog update as per config')
    else:
        epab.utils.ensure_exe('git')
        epab.utils.ensure_exe('gitchangelog')
        LOGGER.info('writing changelog')
        if auto_next_version:
            next_version = epab.utils.get_next_version()
        with gitchangelog_config():
            with temporary_tag(next_version):
                changelog, _ = elib_run.run('gitchangelog', mute=True)
        # changelog = changelog.encode('utf8').replace(b'\r\n', b'\n').decode('utf8')
        changelog = re.sub(BOGUS_LINE_PATTERN, '\\1\n', changelog)
        Path(config.CHANGELOG_FILE_PATH()).write_text(changelog, encoding='utf8')
        if amend:
            CTX.repo.amend_commit(
                append_to_msg='update changelog [auto]', files_to_add=str(config.CHANGELOG_FILE_PATH())
            )
        elif stage:
            CTX.repo.stage_subset(str(config.CHANGELOG_FILE_PATH()))


@click.command()
@click.option('-a', '--amend', is_flag=True, help='Amend last commit')
@click.option('-s', '--stage', is_flag=True, help='Stage changed files')
@click.option('-n', '--next_version', default=None, help='Indicates next version')
@click.option('-anv', '--auto_next_version', default=False, is_flag=True, help='Auto-nump version')
def chglog(amend: bool = False, stage: bool = False, next_version: str = None, auto_next_version: bool = False):
    """
    Writes the changelog

    Args:
        amend: amend last commit with changes
        stage: stage changes
        next_version: indicates next version
        auto_next_version: infer next version from VCS
    """
    changed_files = CTX.repo.changed_files()
    changelog_file_path: Path = config.CHANGELOG_FILE_PATH()
    changelog_file_name = changelog_file_path.name
    if changelog_file_name in changed_files:
        LOGGER.error('changelog has changed; cannot update it')
        exit(-1)
    _chglog(amend, stage, next_version, auto_next_version)
