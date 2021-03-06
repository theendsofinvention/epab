# coding=utf-8

import os

from setuptools import find_packages, setup

requirements = [
    'click',
    'wheel',
    'twine',
    # 'autopep8',
    'pylint',
    'isort',
    'safety',
    'flake8',
    'coverage',
    'hypothesis',
    'pytest-cache',
    'pytest-cov',
    'pytest-vcr',
    'pytest-pycharm',
    'pytest',
    'gitchangelog',
    'gitpython',
    'mockito',
    'setuptools-scm',
    'certifi',
    'pefile',
    'mypy',
    'toml',
    'sarge',
    'pytest-repeat',
    'pytest-faker',
    'pytest-watch',
    'pytest-deadfixtures',
    'bandit',
    'elib_config',
    'elib_run',
    'pystache',
]
test_requirements = []

CLASSIFIERS = filter(None, map(str.strip,
                               """
Development Status :: 3 - Alpha
Topic :: Utilities
License :: OSI Approved :: MIT License
Environment :: Win32 (MS Windows)
Natural Language :: English
Operating System :: Microsoft :: Windows
Operating System :: Microsoft :: Windows :: Windows 7
Operating System :: Microsoft :: Windows :: Windows 8
Operating System :: Microsoft :: Windows :: Windows 8.1
Operating System :: Microsoft :: Windows :: Windows 10
Programming Language :: Cython
Programming Language :: Python
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation
Programming Language :: Python :: Implementation :: CPython
Topic :: Games/Entertainment
Topic :: Utilities
""".splitlines()))


def read_local_files(*file_paths: str) -> str:
    """
    Reads one or more text files and returns them joined together.
    A title is automatically created based on the file name.

    Args:
        *file_paths: list of files to aggregate

    Returns: content of files
    """

    def _read_single_file(file_path):
        with open(file_path) as f:
            filename = os.path.splitext(file_path)[0]
            title = f'{filename}\n{"=" * len(filename)}'
            return '\n\n'.join((title, f.read()))

    return '\n' + '\n\n'.join(map(_read_single_file, file_paths))


entry_points = '''
[console_scripts]
epab=epab.__main__:cli
'''

setup(
    name='EPAB',
    author='132nd-etcher',
    zip_safe=False,
    author_email='epab@daribouca.net',
    platforms=['win32'],
    url=r'https://github.com/132nd-etcher/EPAB',
    download_url=r'https://github.com/132nd-etcher/EPAB/releases',
    description="Etcher's Python Application Builder",
    license='GPLv3',
    long_description=read_local_files('README.md'),
    packages=find_packages(),
    package_data={
        'epab': 'test'
    },
    include_package_data=True,
    entry_points=entry_points,
    install_requires=requirements,
    tests_require=test_requirements,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    python_requires='>=3.6',
    classifiers=CLASSIFIERS,
)
