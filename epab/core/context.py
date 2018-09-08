# coding=utf-8
"""
Global runtime CTX
"""

import os
import typing

from epab.bases.repo import BaseRepo


class CTX:
    """
    Global EPAB context
    """
    run_once: dict = {}
    known_executables: dict = {}
    repo: BaseRepo
    next_version: typing.Optional[str] = None
    stash: bool = False
    appveyor: typing.Optional[str] = os.getenv('APPVEYOR')
    prefix: str = 'EPAB'

    @staticmethod
    def _reset():
        CTX.known_executables = {}
        CTX.run_once = {}
        CTX.repo = None
        CTX.next_version = None
        CTX.stash = False
        CTX.appveyor = False
        CTX.prefix = 'EPAB'
