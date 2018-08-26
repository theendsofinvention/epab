# coding=utf-8
"""
Builds documentation
"""

import click


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


@click.command()
def doc():
    """
    Builds documentation
    """
    raise NotImplementedError
