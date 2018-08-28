# coding=utf-8


from pathlib import Path

import elib_run
from mockito import when

from epab import __version__
from epab.cmd._install_hooks import _install_hooks, _make_venv_path


def test_git_hooks_venv():
    when(elib_run).run('pipenv --venv', filters='Courtesy Notice:').thenReturn(('.', 0))
    Path('./Scripts').mkdir()
    venv = _make_venv_path()
    assert venv.startswith('/'), venv
    assert ':' not in venv, venv
    assert venv.endswith('/Scripts'), venv


def test_git_hooks():
    Path('./.git/hooks').mkdir(parents=True)
    pre_push = Path('./.git/hooks/pre-push')
    assert not pre_push.exists()
    when(elib_run).run('pipenv --venv', filters='Courtesy Notice:').thenReturn(('.', 0))
    _install_hooks()
    assert pre_push.exists()
    assert f'# This Git hook was installed by EPAB {__version__}\n' in pre_push.read_text()
