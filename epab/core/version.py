# coding=utf-8
"""
EPAB current version
"""

import sys

from pkg_resources import DistributionNotFound, get_distribution

from epab.utils._exe_version import get_product_version

try:
    VERSION = get_distribution('epab').version
except DistributionNotFound:  # pragma: no cover
    if getattr(sys, 'frozen', False):
        VERSION = get_product_version(sys.executable)
    else:
        # package is not installed
        VERSION = 'not installed'
