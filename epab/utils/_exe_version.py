# coding=utf-8
"""
Get version info from executable
"""
import typing
from pathlib import Path

import pefile


def _low_word(dword):
    return dword & 0x0000ffff


def _high_word(dword):
    return dword >> 16


class VersionInfo:
    """
    Simple version info
    """

    def __init__(self, file_version, full_version):
        self._file_version = file_version
        self._full_version = full_version

    @property
    def file_version(self) -> str:
        """
        Returns: simple version
        """
        return self._file_version

    @property
    def full_version(self) -> str:
        """
        Returns: full version
        """
        return self._full_version

    def __repr__(self):
        return f'{self.__class__.__name__}({self.file_version}, {self.full_version})'

    def __str__(self):
        return self.file_version


def get_product_version(path: typing.Union[str, Path]) -> VersionInfo:
    """
    Get version info from executable

    Args:
        path: path to the executable

    Returns: VersionInfo
    """
    path = Path(path).absolute()
    pe_info = pefile.PE(str(path))

    for file_info in pe_info.FileInfo:
        if file_info.Key == b'StringFileInfo':
            for string in file_info.StringTable:
                if b'FileVersion' in string.entries.keys():
                    file_version = string.entries[b'SpecialBuild'].decode('utf8')
                    full_version = string.entries[b'PrivateBuild'].decode('utf8')
                    return VersionInfo(file_version, full_version)

    raise RuntimeError(f'unable to obtain version from {path}')
