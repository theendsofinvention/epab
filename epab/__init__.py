# coding=utf-8
"""
This script automates linting, testing and releasing of Python apps locally and on Appveyor

It is intended for my personal use only
"""
from ._e_version import get_versions
__version__ = get_versions()['version']
del get_versions
