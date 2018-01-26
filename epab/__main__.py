# coding=utf-8

# coding=utf-8
"""
Collections of tools to build a python app
"""
import os

import click

import epab.cmd
import epab.linters
import epab.utils
from epab.core import CONFIG, CTX, VERSION

# def _install_pyinstaller(ctx: click.Context, force: bool = False):
#     """
#     Installs pyinstaller package from a custom repository
#
#     The latest official master branch of Pyinstaller does not work with the version of Python I'm using at this time
#
#     Args:
#         ctx: lick context (passed automatically by Click)
#         force: uses "pip --upgrade" to force the installation of this specific version of PyInstaller
#     """
#     # noinspection SpellCheckingInspection
#     repo = r'git+https://github.com/132nd-etcher/pyinstaller.git@develop#egg=pyinstaller==3.3.dev0+g2fcbe0f'
#     if force:
#         # epab.utils.do(ctx, ['pip', 'install', '--upgrade', repo])
#         epab.utils.run(f'pip install --upgrade {repo}')
#     else:
#         epab.utils.run(f'pip install {repo}')


# noinspection PyUnusedLocal
def _print_version(ctx: click.Context, _, value):

    if not value or ctx.resilient_parsing:
        return

    print(VERSION)
    exit(0)


# noinspection PyUnusedLocal
def _next_version(ctx: click.Context, _, value):

    CONFIG.quiet = True

    if not value or ctx.resilient_parsing:
        return

    print(epab.utils.get_git_version_info())
    exit(0)


# @click.group(invoke_without_command=True)
@click.group(chain=True)
@click.option('-v', '--version',
              is_flag=True, is_eager=True, expose_value=False, callback=_print_version, default=False,
              help='Print version and exit')
@click.option('-nv', '--next-version',
              is_flag=True, is_eager=True, expose_value=False, callback=_next_version, default=False,
              help='Print next version and exit')
@click.option('-n', '--dry-run', is_flag=True, default=False, help='Dry run')
@click.option('-d', '--dirty', is_flag=True, default=False, help='Allow dirty repository')
@click.option('-ns', '--no-stash', 'stash', is_flag=True, default=True, help='No stashing')
def cli(dry_run, dirty, stash):
    """
    This is a tool that handles all the tasks to build a Python application

    This tool is installed as a setuptools entry point, which means it should be accessible from your terminal once
    this application is installed in develop mode.

    Just activate your venv and type the following in whatever shell you fancy:
    """
    epab.utils.info(f'EPAB {VERSION}')
    epab.utils.info(f'Running in {os.getcwd()}')
    CONFIG.load()
    CTX.dry_run = dry_run
    CTX.repo = epab.utils.Repo()
    CTX.repo.ensure()
    CTX.stash = stash
    if not dirty and CTX.repo.is_dirty():
        click.secho('Repository is dirty', err=True, fg='red')
        exit(-1)


# @cli.command()
# @click.option('-s', '--show', is_flag=True, help='Show the doc in browser')
# @click.option('-c', '--clean', is_flag=True, help='Clean build')
# @click.option('-p', '--publish', is_flag=True, help='Upload doc')
# @click.pass_context
# def doc(ctx, show, clean_, publish):
#     """
#     Builds the documentation using Sphinx (http://www.sphinx-doc.org/en/stable)
#     """
#     if clean_ and os.path.exists('./doc/html'):
#         shutil.rmtree('./doc/html')
#     if os.path.exists('./doc/api'):
#         shutil.rmtree('./doc/api')
#     epab.utils.do(ctx, [
#         'sphinx-apidoc',
#         CONFIG['package'],
#         '-o', 'doc/api',
#         '-H', f'{CONFIG["package"]} API',
#         '-A', '132nd-etcher',
#         '-V', f'{ctx.obj["semver"]}\n({ctx.obj["pep440"]})',
#         # '-P',
#         '-f',
#     ])
#     epab.utils.do(ctx, [
#         'sphinx-build',
#         '-b',
#         'html',
#         'doc',
#         'doc/html'
#     ])
#     if show:
#         webbrowser.open_new_tab(
#             f'file://{os.path.abspath("./doc/html/index.html")}')
#     if publish:
#         output_filter = [
#             'warning: LF will be replaced by CRLF',
#             'The file will have its original line endings',
#             'Checking out files:'
#         ]
#         if not os.path.exists(f'./{CONFIG["package"]}-doc'):
#             epab.utils.do(ctx, ['git', 'clone', CONFIG['doc_repo']],
#                           filter_output=output_filter)
#         with epab.utils.temporary_working_dir(CONFIG['doc_folder']):
#             epab.utils.do(ctx, ['git', 'pull'])
#             if os.path.exists('./docs'):
#                 shutil.rmtree('./docs')
#             shutil.copytree('../doc/html', './docs')
#             epab.utils.do(ctx, ['git', 'add', '.'], filter_output=output_filter)
#             epab.utils.do(ctx, ['git', 'commit', '-m', 'automated doc build'],
#                           filter_output=output_filter)
#             epab.utils.do(ctx, ['git', 'push'], filter_output=output_filter)


_LINTERS = [
    epab.linters.pep8,
    epab.linters.flake8,
    epab.linters.isort,
    epab.linters.pylint,
    epab.linters.safety,
    epab.linters.lint,
]

_COMMANDS = [
    epab.cmd.reqs,
    epab.cmd.release,
    epab.cmd.chglog,
    epab.cmd.pytest,
    epab.cmd.install_hooks,
]


for command in _COMMANDS + _LINTERS:
    cli.add_command(command)
