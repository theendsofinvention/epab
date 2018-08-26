# coding=utf-8
"""
This script automates linting, testing and releasing of Python apps locally and on Appveyor

It is intended for my personal use only
"""

import sys

from pkg_resources import DistributionNotFound, get_distribution

from epab.utils import get_product_version

if getattr(sys, 'frozen', False):
    __version__ = get_product_version(sys.executable).file_version
else:
    try:
        __version__ = get_distribution('epab').version
    except DistributionNotFound:  # pragma: no cover
        # package is not installed
        __version__ = 'not installed'
