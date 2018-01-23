# coding=utf-8
"""
Click command to write the requirements
"""

import click
import epab.utils


@epab.utils.run_once
def _write_reqs(ctx, auto_commit: bool):
    """
    Writes the requirement files

    Args:
        auto_commit: whether or not to commit the changes
    """

    def _write_reqs_file(cmd, file_path):
        epab.utils.info(f'Writing {file_path}')
        output, err, code = epab.utils.do_ex(ctx, cmd)
        if code:
            if err:
                epab.utils.error(err)
            exit(code)
        with open(file_path, 'w') as stream:
            stream.write(output)

    epab.utils.info('Writing requirements')
    base_cmd = ['pipenv', 'lock', '-r']
    _write_reqs_file(base_cmd, 'requirements.txt')
    _write_reqs_file(base_cmd + ['-d'], 'requirements-dev.txt')
    if auto_commit:
        files_to_add = ['Pipfile', 'requirements.txt', 'requirements-dev.txt']
        epab.utils.repo_commit(ctx, message='chg: dev: update requirements [auto]', files_to_add=files_to_add)


@click.command()
@click.option('-c', '--auto-commit', is_flag=True, help='Commit the changes')
@click.pass_context
def reqs(ctx: click.Context, auto_commit: bool):
    """
    Write requirements files
    """
    _write_reqs(ctx, auto_commit)
