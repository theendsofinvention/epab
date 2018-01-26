# coding=utf-8
"""
EPAB current version
"""


from pkg_resources import DistributionNotFound, get_distribution

try:
    VERSION = get_distribution('epab').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    VERSION = 'not installed'
