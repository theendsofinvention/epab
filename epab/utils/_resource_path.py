# coding=utf-8
"""
Get absolute path to resource, works for dev and for PyInstaller
"""

import sys
import typing
from pathlib import Path

import pkg_resources


def _get_from_dev(package_name: str, relative_path: Path) -> Path:
    return Path(package_name, relative_path).absolute()


def _get_from_sys(_: str, relative_path: Path) -> Path:
    return Path(getattr(sys, '_MEIPASS', '.'), relative_path).absolute()


def _get_from_package(package_name: str, relative_path: Path) -> Path:
    return Path(pkg_resources.resource_filename(package_name, str(relative_path))).absolute()


def resource_path(package_name: str, relative_path: typing.Union[str, Path]) -> Path:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    relative_path = Path(relative_path)
    methods = [
        _get_from_dev,
        _get_from_package,
        _get_from_sys,
    ]
    for method in methods:
        path = method(package_name, relative_path)
        if path.exists():
            return path

    raise FileNotFoundError(relative_path)
