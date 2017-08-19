# coding=utf-8

import os

from setuptools import setup


def read_local_files(*file_paths: str) -> str:
    """
    Reads one or more text files and returns them joined together.

    A title is automatically created based on the file name.

    :param file_paths: list of files to aggregate

    """

    def _read_single_file(file_path):
        with open(file_path) as f:
            filename = os.path.splitext(file_path)[0]
            title = f'{filename}\n{"=" * len(filename)}'
            return '\n\n'.join((title, f.read()))

    return '\n' + '\n\n'.join(map(_read_single_file, file_paths))


dependency_links = []

# noinspection SpellCheckingInspection
install_requires = [
    'pyyaml',
    'click',
]

# noinspection SpellCheckingInspection
test_requires = [
    'pytest',
    'coverage',
    'hypothesis',
    'pytest-cache',
    'pytest-catchlog',
    'pytest-cov',
    'pytest-mock',
    'pytest-pep8',
    'pytest-pycharm',
]

dev_requires = []

setup_requires = [
    'setuptools_scm',
]

entry_points = '''
[console_scripts]
epab=epab:cli
'''

if __name__ == '__main__':
    setup(
        name='EPAB',
        author='132nd-etcher',
        zip_safe=False,
        author_email='epab@daribouca.net',
        platforms=['win32'],
        url=r'https://github.com/132nd-etcher/EPAB',
        download_url=r'https://github.com/132nd-etcher/EPAB/releases',
        description='Set of tools for the DCS mission builder',
        license='GPLv3',
        py_modules=['epab'],
        long_description=read_local_files('README.rst', 'CHANGELOG.rst'),
        packages=['epab'],
        include_package_data=True,
        install_requires=install_requires,
        entry_points=entry_points,
        tests_require=test_requires,
        use_scm_version=True,
        setup_requires=setup_requires,
        dependency_links=dependency_links,
        python_requires='>=3.6',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Topic :: Utilities',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Environment :: Win32 (MS Windows)',
            'Natural Language :: English',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: Microsoft :: Windows :: Windows 7',
            'Operating System :: Microsoft :: Windows :: Windows 8',
            'Operating System :: Microsoft :: Windows :: Windows 8.1',
            'Operating System :: Microsoft :: Windows :: Windows 10',
            'Programming Language :: Cython',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: Games/Entertainment',
            'Topic :: Utilities',
        ],
    )
