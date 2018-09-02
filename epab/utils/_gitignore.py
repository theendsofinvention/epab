# coding=utf-8
"""
Manages .gitignore file
"""

from pathlib import Path

GIT_IGNORE = Path('.gitignore').absolute()


def add_to_gitignore(line: str):
    """
    Adds a line to the .gitignore file of the repo

    Args:
        line: line to add
    """
    if not line.endswith('\n'):
        line = f'{line}\n'
    if GIT_IGNORE.exists():
        if line in GIT_IGNORE.read_text(encoding='utf8'):
            return
        previous_content = GIT_IGNORE.read_text(encoding='utf8')
    else:
        previous_content = ''
    GIT_IGNORE.write_text(previous_content + line, encoding='utf8')
