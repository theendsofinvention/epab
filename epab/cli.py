# coding=utf-8

# coding=utf-8
"""
Collections of tools to build a python app
"""
import importlib
import os
import re
import shutil
import sys
import webbrowser
from contextlib import contextmanager

import click
import yaml
from pkg_resources import DistributionNotFound, get_distribution
from setuptools_scm import get_version

from epab.do import do, do_ex, find_executable

try:
    __version__ = get_distribution('epab').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'

with open('epab.yml') as config_file:
    CONFIG = yaml.load(config_file)


@contextmanager
def temporary_working_dir(path):
    """
    Context to temporarily change the working directory

    Args:
        path: working directory to cd into
    """
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


def repo_is_dirty(ctx) -> bool:
    """
    Checks if the current repository contains uncommitted or untracked changes

    Returns: true if the repository is clean
    """
    out, _, _ = do_ex(ctx, ['git', 'status', '--porcelain', '--untracked-files=no'])
    return bool(out)


def repo_get_branch(ctx) -> str:
    return do(ctx, 'git rev-parse --abbrev-ref HEAD', mute_stdout=True)


def repo_get_latest_tag(ctx) -> str:
    return do(ctx, 'git describe --abbrev=0 --tags', mute_stdout=True)


def ensure_repo():
    """
    Makes sure the current working directory is a Git repository.
    """
    if not os.path.exists('.git') or not os.path.exists(CONFIG['package']):
        click.secho('This command is meant to be ran in a Git repository.\n'
                    'You can clone the repository by running:\n\n'
                    f'\tgit clone https://github.com/132nd-etcher/{CONFIG["package"]}.git\n\n'
                    'Then cd into it and try again.',
                    fg='red', err=True)
        exit(-1)


def ensure_module(ctx, module_name: str, import_name: str = None):
    """
    Makes sure that a module is importable.

    In case the module cannot be found, print an error and exit.

    Args:
        import_name: name to use while trying to import
        module_name: name of the module if install is needed
    """
    if import_name is None:
        import_name = module_name
    try:
        importlib.import_module(import_name)
    except ModuleNotFoundError:
        do(ctx, ['pip', 'install', module_name])


def _write_requirements(ctx: click.Context, packages_list, outfile, prefix_list=None):
    with open('temp', 'w') as source_file:
        source_file.write('\n'.join(packages_list))
    packages, _, _ = do_ex(
        ctx,
        [
            'pip-compile',
            '--index',
            '--upgrade',
            '--annotate',
            '--no-header',
            '-n',
            'temp'
        ]
    )
    os.remove('temp')
    with open(outfile, 'w') as req_file:
        if prefix_list:
            for prefix in prefix_list:
                req_file.write(f'{prefix}\n')
        for package in packages.splitlines():
            req_file.write(f'{package}\n')


def _install_pyinstaller(ctx: click.Context, force: bool = False):
    """
    Installs pyinstaller package from a custom repository

    The latest official master branch of Pyinstaller does not work with the version of Python I'm using at this time

    Args:
        ctx: lick context (passed automatically by Click)
        force: uses "pip --upgrade" to force the installation of this specific version of PyInstaller
    """
    repo = r'git+https://github.com/132nd-etcher/pyinstaller.git@develop#egg=pyinstaller==3.3.dev0+g2fcbe0f'
    if force:
        do(ctx, ['pip', 'install', '--upgrade', repo])
    else:
        do(ctx, ['pip', 'install', repo])


def _get_version():
    try:
        return get_distribution(CONFIG['package']).version
    except DistributionNotFound:
        return 'not installed'


# noinspection PyUnusedLocal
def _print_version(ctx: click.Context, _, value):
    if not value or ctx.resilient_parsing:
        return

    ensure_repo()

    click.secho(__version__, fg='green')
    exit(0)


# @click.group(invoke_without_command=True)
@click.group(chain=True)
@click.option('-v', '--version',
              is_flag=True, is_eager=True, expose_value=False, callback=_print_version, default=False,
              help='Print version and exit')
@click.pass_context
def cli(ctx):
    """
    This is a tool that handles all the tasks to build a Python application

    This tool is installed as a setuptools entry point, which means it should be accessible from your terminal once
    this application is installed in develop mode.

    Just activate your venv and type the following in whatever shell you fancy:
    """
    ctx.obj = {}
    ensure_repo()
    click.secho(f'EPAB {__version__}', fg='green')


@cli.command()
@click.option('--prod/--no-prod', default=True, help='Whether or not to write "requirement.txt"')
@click.option('--test/--no-test', default=True, help='Whether or not to write "requirement-test.txt"')
@click.option('--dev/--no-dev', default=True, help='Whether or not to write "requirement-dev.txt"')
@click.pass_context
def reqs(ctx: click.Context, prod, test, dev):
    """
    Write requirements files
    """
    ensure_module(ctx, 'pip-tools', 'piptools')
    if not find_executable('pip-compile'):
        click.secho('Missing module "pip-tools".\n'
                    'Install it manually with: "pip install pip-tools"\n'
                    'Or install all dependencies with: "pip install -r requirements-dev.txt"',
                    err=True, fg='red')
        exit(-1)
    try:
        sys.path.insert(0, '.')
        if prod:
            from setup import install_requires
            _write_requirements(
                ctx,
                packages_list=install_requires,
                outfile='requirements.txt'
            )
        if test:
            from setup import test_requires
            _write_requirements(
                ctx,
                packages_list=test_requires,
                outfile='requirements-test.txt',
                prefix_list=['-r requirements.txt']
            )
        if dev:
            from setup import dev_requires
            _write_requirements(
                ctx,
                packages_list=dev_requires,
                outfile='requirements-dev.txt',
                prefix_list=['-r requirements.txt', '-r requirements-test.txt']
            )
    finally:
        sys.path.pop(0)


@cli.command()
@click.option('--force', default=False, is_flag=True, help='Force updating changelog"')
@click.pass_context
def chglog(ctx, force):
    """
    Writes the changelog

    Returns:
        bool: returns true if changes have been committed to the repository
    """
    if CONFIG.get('disabled_changelog'):
        click.secho('Skipping changelog', fg='green')
    else:
        tag = do(ctx, 'git describe --tags --always', mute_stdout=True)
        click.secho(f'Git tag: {tag}', fg='green')
        if '-g' in tag and not force:
            click.secho('No tag on this commit, skipping changelog update', err=True, fg='red')
            return
        ensure_module(ctx, 'gitchangelog')
        find_executable('git')
        changelog = do(ctx, ['gitchangelog'], mute_stdout=True)
        with open('CHANGELOG.rst', mode='w') as handle:
            handle.write(re.sub(r'(\s*\r\n){2,}', '\r\n', changelog))


@cli.command()
@click.pass_context
def pytest(ctx):
    """
    Runs Pytest (https://docs.pytest.org/en/latest/)
    """
    ensure_module(ctx, 'pytest')
    if os.environ.get('APPVEYOR'):
        runner = CONFIG['test']['av_runner']
    else:
        runner = CONFIG['test']['runner']
    do(ctx, runner)


@cli.command()
@click.pass_context
def flake8(ctx):
    """
    Runs Flake8 (http://flake8.pycqa.org/en/latest/)
    """
    ensure_module(ctx, 'flake8')
    do(ctx, ['flake8'])


@cli.command()
@click.pass_context
def isort(ctx):
    """
    Runs Flake8 (http://flake8.pycqa.org/en/latest/)
    """
    ensure_module(ctx, 'isort')
    do(ctx, ['isort', '-rc', '.'])


@cli.command()
@click.pass_context
def prospector(ctx):
    """
    Runs Landscape.io's Prospector (https://github.com/landscapeio/prospector)

    This includes flake8 & Pylint
    """
    ensure_module(ctx, 'prospector')
    do(ctx, ['prospector'])


@cli.command()
@click.pass_context
@click.argument('src', type=click.Path(exists=True), default=CONFIG['package'])
@click.option('-r', '--reports', is_flag=True, help='Display full report')
@click.option('-f', '--format', 'format_',
              type=click.Choice(['text', 'parseable', 'colorized', 'json']), default='colorized')
def pylint(ctx, src, reports, format_):
    """
    Analyze a given python SRC (module or package) with Pylint (SRC must exist)

    Default module: CONFIG['package']
    """
    ensure_module(ctx, 'pylint')
    cmd = ['pylint', src, f'--output-format={format_}']
    if reports:
        cmd.append('--reports=y')
    do(ctx, cmd)


@cli.command()
@click.pass_context
def safety(ctx):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    ensure_module(ctx, 'safety')
    do(ctx, ['safety', 'check', '--bare'])


@cli.command()
@click.pass_context
def autopep8(ctx):
    """
    Runs Pyup's Safety tool (https://pyup.io/safety/)
    """
    ensure_module(ctx, 'autopep8')
    do(ctx, ['autopep8', '-r', '--in-place', '.'])


@cli.command()
@click.option('-s', '--show', is_flag=True, help='Show the doc in browser')
@click.option('-c', '--clean', is_flag=True, help='Clean build')
@click.option('-p', '--publish', is_flag=True, help='Upload doc')
@click.pass_context
def doc(ctx, show, clean_, publish):
    """
    Builds the documentation using Sphinx (http://www.sphinx-doc.org/en/stable)
    """
    if clean_ and os.path.exists('./doc/html'):
        shutil.rmtree('./doc/html')
    if os.path.exists('./doc/api'):
        shutil.rmtree('./doc/api')
    do(ctx, [
        'sphinx-apidoc',
        CONFIG['package'],
        '-o', 'doc/api',
        '-H', f'{CONFIG["package"]} API',
        '-A', '132nd-etcher',
        '-V', f'{ctx.obj["semver"]}\n({ctx.obj["pep440"]})',
        # '-P',
        '-f',
    ])
    do(ctx, [
        'sphinx-build',
        '-b',
        'html',
        'doc',
        'doc/html'
    ])
    if show:
        webbrowser.open_new_tab(f'file://{os.path.abspath("./doc/html/index.html")}')
    if publish:
        output_filter = [
            'warning: LF will be replaced by CRLF',
            'The file will have its original line endings',
            'Checking out files:'
        ]
        if not os.path.exists(f'./{CONFIG["package"]}-doc'):
            do(ctx, ['git', 'clone', CONFIG['doc_repo']], filter_output=output_filter)
        with temporary_working_dir(CONFIG['doc_folder']):
            do(ctx, ['git', 'pull'])
            if os.path.exists('./docs'):
                shutil.rmtree('./docs')
            shutil.copytree('../doc/html', './docs')
            do(ctx, ['git', 'add', '.'], filter_output=output_filter)
            do(ctx, ['git', 'commit', '-m', 'automated doc build'], filter_output=output_filter)
            do(ctx, ['git', 'push'], filter_output=output_filter)


@cli.command()
def clean():
    """
    Cleans up build dir
    """
    folders_to_cleanup = [
        '.eggs',
        'build',
        f'{CONFIG["package"]}.egg-info',
    ]
    for folder in folders_to_cleanup:
        if os.path.exists(folder):
            click.secho(f'Removing: {folder}', fg='green')
            shutil.rmtree(folder)


@cli.command()
@click.pass_context
def pre_build(ctx):
    if ctx.obj.get('pre_build'):
        return
    if repo_is_dirty(ctx):
        click.secho('Repository is dirty', err=True, fg='red')
        exit(1)
    if repo_get_branch(ctx) != 'master':
        click.secho('Not on master branch', err=True, fg='red')
        exit(1)
    tag = do(ctx, 'git describe --tags --always', mute_stdout=True)
    click.secho(f'Git tag: {tag}', fg='green')
    if '-g' in tag:
        click.secho('No tag on this commit', err=True, fg='red')
        exit(1)
    version = get_version()
    if '+' in version:
        click.secho(f'Invalid version tag: {tag}', err=True, fg='red')
        exit(1)
    click.secho(f'Version: {version}', fg='green')
    ctx.obj['pre_build'] = 'done'


@cli.command()
@click.pass_context
def wheel(ctx):
    """
    Builds wheels
    """
    ctx.invoke(pre_build)
    do(ctx, sys.executable.replace('\\', '/') + ' setup.py bdist_wheel')
    ctx.invoke(clean)


@cli.command()
@click.pass_context
def sdist(ctx):
    """
    Builds wheels
    """
    ctx.invoke(pre_build)
    do(ctx, sys.executable.replace('\\', '/') + ' setup.py sdist')
    ctx.invoke(clean)


@cli.command()
@click.pass_context
def upload(ctx):
    """
    Builds wheels
    """
    do(ctx, 'twine upload dist/* --skip-existing', mute_stdout=True, mute_stderr=True)


@cli.command()
@click.pass_context
def pre_push(ctx):
    """
    This is meant to be used as a Git pre-push hook
    """
    ctx.invoke(clean)
    ctx.invoke(autopep8)
    ctx.invoke(isort)
    ctx.invoke(flake8)
    ctx.invoke(pylint)
    ctx.invoke(reqs)
    ctx.invoke(chglog)
    ctx.invoke(safety)
    if repo_is_dirty(ctx):
        click.secho('Repository is dirty', err=True, fg='red')
        exit(-1)
    click.secho('All good!', fg='green')
