# coding=utf-8
"""
Convenience methods for AV
"""
import subprocess  # nosec

import elib_run


class AV:
    """
    Convenience methods for AV
    """

    @staticmethod
    def _out(level, msg: str, details: str = None):
        if level not in ('Information', 'Error'):
            raise ValueError(f'unknown level: {level}')
        if details:
            subprocess.call(f'appveyor AddMessage "{msg}" -Category {level} -Details "{details}"')  # nosec
        else:
            subprocess.call(f'appveyor AddMessage "{msg}" -Category {level}')  # nosec

    @staticmethod
    def info(msg: str, details: str = None):
        """
        Prints message to AV

        Args:
            msg: message
            details: message details
        """
        AV._out('Information', msg, details)

    @staticmethod
    def error(msg: str, details: str = None):
        """
        Prints error to AV

        Args:
            msg: error
            details: error details
        """
        AV._out('Error', msg, details)

    @staticmethod
    def update_build_version(build_version: str):
        """
        Update AV build version

        Args:
            build_version: new version
        """
        elib_run.run(f'appveyor UpdateBuild -Version {build_version}')

    @staticmethod
    def set_env_var(key: str, value: str):
        """
        Sets environment variable on AV

        Args:
            key: variable name
            value: variable value
        """
        elib_run.run(f'appveyor SetVariable -Name {key} -Value {value}')
        AV.info('Env', f'set "{key}" -> "{value}"')
