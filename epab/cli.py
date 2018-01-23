# coding=utf-8

# coding=utf-8
"""
Collections of tools to build a python app
"""
import os
import shutil
import webbrowser

import click
import epab.cmd
import epab.linters
import epab.linters._lint
import epab.utils
import yaml
from epab import __version__

with open('epab.yml') as config_file:
    CONFIG = yaml.safe_load(config_file)


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
        epab.utils.do(ctx, ['pip', 'install', '--upgrade', repo])
    else:
        epab.utils.do(ctx, ['pip', 'install', repo])


def _initiliaze_context_object():
    return {
        'CONFIG': CONFIG,
        'run_once': {},
        'dry_run': False,
    }


# noinspection PyUnusedLocal
def _print_version(ctx: click.Context, _, value):
    ctx.obj = _initiliaze_context_object()

    if not value or ctx.resilient_parsing:
        return

    epab.utils.info(__version__)
    exit(0)


# @click.group(invoke_without_command=True)
@click.group(chain=True)
@click.option('-v', '--version',
              is_flag=True, is_eager=True, expose_value=False, callback=_print_version, default=False,
              help='Print version and exit')
@click.option('-n', '--dry-run', is_flag=True, default=False, help='Dry run')
@click.option('-d', '--dirty', is_flag=True, default=False, help='Allow dirty repository')
@click.pass_context
def cli(ctx, dry_run, dirty):
    """
    This is a tool that handles all the tasks to build a Python application

    This tool is installed as a setuptools entry point, which means it should be accessible from your terminal once
    this application is installed in develop mode.

    Just activate your venv and type the following in whatever shell you fancy:
    """
    ctx.obj = _initiliaze_context_object()
    ctx.obj['dry_run'] = dry_run
    epab.utils.info(f'EPAB {__version__}')
    epab.utils.repo_ensure(ctx)
    if not dirty and epab.utils.repo_is_dirty(ctx):
        click.secho('Repository is dirty', err=True, fg='red')
        exit(-1)


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
    epab.utils.do(ctx, [
        'sphinx-apidoc',
        CONFIG['package'],
        '-o', 'doc/api',
        '-H', f'{CONFIG["package"]} API',
        '-A', '132nd-etcher',
        '-V', f'{ctx.obj["semver"]}\n({ctx.obj["pep440"]})',
        # '-P',
        '-f',
    ])
    epab.utils.do(ctx, [
        'sphinx-build',
        '-b',
        'html',
        'doc',
        'doc/html'
    ])
    if show:
        webbrowser.open_new_tab(
            f'file://{os.path.abspath("./doc/html/index.html")}')
    if publish:
        output_filter = [
            'warning: LF will be replaced by CRLF',
            'The file will have its original line endings',
            'Checking out files:'
        ]
        if not os.path.exists(f'./{CONFIG["package"]}-doc'):
            epab.utils.do(ctx, ['git', 'clone', CONFIG['doc_repo']],
                          filter_output=output_filter)
        with epab.utils.temporary_working_dir(CONFIG['doc_folder']):
            epab.utils.do(ctx, ['git', 'pull'])
            if os.path.exists('./docs'):
                shutil.rmtree('./docs')
            shutil.copytree('../doc/html', './docs')
            epab.utils.do(ctx, ['git', 'add', '.'], filter_output=output_filter)
            epab.utils.do(ctx, ['git', 'commit', '-m', 'automated doc build'],
                          filter_output=output_filter)
            epab.utils.do(ctx, ['git', 'push'], filter_output=output_filter)


cli.add_command(epab.linters.pep8)
cli.add_command(epab.linters.flake8)
cli.add_command(epab.linters.isort)
cli.add_command(epab.linters.pylint)
cli.add_command(epab.linters.safety)
cli.add_command(epab.linters.lint)
cli.add_command(epab.cmd.reqs)
cli.add_command(epab.cmd.release)
cli.add_command(epab.cmd.chglog)
cli.add_command(epab.cmd.appveyor)
cli.add_command(epab.cmd.pytest)
