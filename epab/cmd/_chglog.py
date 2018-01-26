# coding=utf-8
"""
Updates CHANGELOG.rst with the latest commits
"""

import re
from pathlib import Path

import click

import epab.utils
from epab.core import CONFIG, CTX

BOGUS_LINE_PATTERN = re.compile('^(- .*)(\n){2}', flags=re.MULTILINE)


@epab.utils.run_once
@epab.utils.stashed
def _chglog(amend: bool = False, stage: bool = False):
    """
    Writes the changelog

    Args:
        amend: amend last commit with changes
        stage: stage changes
    """
    if CONFIG.changelog__disable:
        epab.utils.info('Skipping changelog update as per config')
    else:
        epab.utils.ensure_exe('git')
        epab.utils.ensure_exe('gitchangelog')
        epab.utils.info('Writing changelog')
        changelog, _ = epab.utils.run('gitchangelog', mute=True)
        changelog = changelog.encode('utf8').replace(b'\r\n', b'\n').decode('utf8')
        changelog = re.sub(BOGUS_LINE_PATTERN, '\\1\n', changelog)
        Path(CONFIG.changelog__file).write_text(changelog, encoding='utf8')
        if amend:
            CTX.repo.amend_commit(append_to_msg='update changelog [auto]', files_to_add=CONFIG.changelog__file)
        elif stage:
            CTX.repo.stage_subset(CONFIG.changelog__file)


@click.command()
@click.option('-a', '--amend', is_flag=True, help='Amend last commit')
@click.option('-s', '--stage', is_flag=True, help='Stage changed files')
def chglog(amend: bool = False, stage: bool = False):
    """
    Writes the changelog

    Args:
        amend: amend last commit with changes
        stage: stage changes
    """
    changed_files = CTX.repo.changed_files()
    if CONFIG.changelog__file in changed_files:
        epab.utils.error('Changelog has changed; cannot update it')
        exit(-1)
    _chglog(amend, stage)
