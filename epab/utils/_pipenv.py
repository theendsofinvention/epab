# coding=utf-8
import importlib

from ._console import _error, _info
from ._do import do, do_ex
from ._repo import repo_commit
from ._run_once import run_once


def ensure_module(ctx, module_name: str, import_name: str = None):
    """
    Makes sure that a module is importable.

    In case the module cannot be found, print an error and exit.

    Args:
        ctx: Click's context
        import_name: name to use while trying to import
        module_name: name of the module if install is needed
    """
    if import_name is None:
        import_name = module_name
    try:
        importlib.import_module(import_name)
    except ModuleNotFoundError:
        do(ctx, ['pip', 'install', module_name])


@run_once
def update_env(ctx):
    _info('Updating environment')
    do(ctx, ['pipenv', 'update', '-d'])


def _write_reqs(ctx, cmd, file_path):
    _info(f'Writing {file_path}')
    reqs, err, code = do_ex(ctx, cmd)
    if code:
        if err:
            _error(err)
        exit(code)
    with open(file_path, 'w') as stream:
        stream.write(reqs)


@run_once
def write_reqs(ctx, auto_commit: bool):
    _info('Writing requirements')
    base_cmd = ['pipenv', 'lock', '-r']
    _write_reqs(ctx, base_cmd, 'requirements.txt')
    _write_reqs(ctx, base_cmd + ['-d'], 'requirements-dev.txt')
    if auto_commit:
        files_to_add = ['Pipfile', 'Pipfile.lock', 'requirements.txt', 'requirements-dev.txt']
        repo_commit(ctx, 'chg: dev: update requirements [auto] [skip ci]', files_to_add=files_to_add)
