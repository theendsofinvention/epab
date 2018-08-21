# coding=utf-8
"""
Get version info from executable
"""
import traceback
import typing
from pathlib import Path

import pefile


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


def _parse_file_info(file_info_list) -> typing.Optional['VersionInfo']:
    for _file_info in file_info_list:
        if _file_info.Key == b'StringFileInfo':  # pragma: no branch
            for string in _file_info.StringTable:  # pragma: no branch
                if b'FileVersion' in string.entries.keys():  # pragma: no branch
                    file_version = string.entries[b'SpecialBuild'].decode('utf8')
                    full_version = string.entries[b'PrivateBuild'].decode('utf8')
                    return VersionInfo(file_version, full_version)
    return None


# pylint: disable=inconsistent-return-statements
def get_product_version(path: typing.Union[str, Path]) -> VersionInfo:
    """
    Get version info from executable

    Args:
        path: path to the executable

    Returns: VersionInfo
    """
    path = Path(path).absolute()
    pe_info = pefile.PE(str(path))

    try:
        for file_info in pe_info.FileInfo:  # pragma: no branch
            if isinstance(file_info, list):
                result = _parse_file_info(file_info)
                if result:
                    return result
            else:
                result = _parse_file_info(pe_info.FileInfo)
                if result:
                    return result

        raise RuntimeError(f'unable to obtain version from {path}')
    except (KeyError, AttributeError) as exc:
        traceback.print_exc()
        raise RuntimeError(f'unable to obtain version from {path}') from exc
