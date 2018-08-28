# coding=utf-8
"""
Installs Git hooks
"""
from pathlib import Path

import click
import elib_run

from epab import __version__

PRE_PUSH = """#!/bin/sh
#
# This Git hook was installed by EPAB {version}
#
PATH="{venv}:$PATH"
echo `epab --version`

epab reqs -a chglog -a

epab -d pytest -l -x --ff
if [ "$?" -ne "0" ]
then
    echo "Tests failed"
    exit 1
fi
exit 0"""

PRE_COMMIT = """#!/bin/sh
#
# This Git hook was installed by EPAB {version}
#
PATH="{venv}:$PATH"
echo `epab --version`

epab -d -ns lint
if [ "$?" -ne "0" ]
then
    echo "Linting error"
    exit 1
fi

exit 0"""


def _make_venv_path() -> str:
    venv, _ = elib_run.run('pipenv --venv', filters='Courtesy Notice:')
    venv_path = Path(venv.rstrip(), 'Scripts').absolute()
    return Path('/', venv_path.parts[0].replace(':', '').lower(), *venv_path.parts[1:]).as_posix()


def _install_hooks():
    venv_path = _make_venv_path()
    Path('./.git/hooks/pre-push').write_text(PRE_PUSH.format(venv=venv_path, version=__version__))
    Path('./.git/hooks/pre-commit').write_text(PRE_COMMIT.format(venv=venv_path, version=__version__))


@click.command()
def install_hooks():
    """
    Install Git hooks
    """
    _install_hooks()
