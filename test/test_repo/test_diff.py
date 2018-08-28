# coding=utf-8
from pathlib import Path

import pytest

from epab.utils._repo import Repo
from epab.core import CTX


def test_diff_no_change(repo: Repo):
    assert '' == repo.diff()


def test_diff_no_file_given(repo: Repo):
    Path('test.file').write_text('test\n')
    assert '' == repo.diff()
    repo.commit('dummy')
    Path('test.file').write_text('changed\n')
    diff = repo.diff()
    assert '--- a/test.file' in diff
    assert '+++ b/test.file' in diff
    assert '-test' in diff
    assert '+changed' in diff


def test_diff_with_files(repo: Repo):
    Path('test.file').write_text('test\n')
    Path('test.file1').write_text('test\n')
    Path('test.file2').write_text('test\n')
    assert '' == repo.diff()
    repo.commit('dummy')
    Path('test.file1').write_text('changed\n')
    Path('test.file2').write_text('changed\n')
    empty_diff = repo.diff('test.file')
    assert '' == empty_diff
    single_diff = repo.diff('test.file1')
    assert '--- a/test.file1' in single_diff
    assert '+++ b/test.file1' in single_diff
    assert '-test' in single_diff
    assert '+changed' in single_diff
