# coding=utf-8
import subprocess

import elib_run
import pytest
from mockito import expect, verifyStubbedInvocationsAreUsed, when

import epab.utils
from epab.core import CTX


def test_av_info():
    CTX.appveyor = True
    when(subprocess).call(f'appveyor AddMessage "message" -Category Information')
    epab.utils.AV.info('message')
    verifyStubbedInvocationsAreUsed()


def test_av_info_details():
    CTX.appveyor = True
    when(subprocess).call(f'appveyor AddMessage "message" -Category Information -Details "details"')
    epab.utils.AV.info('message', 'details')
    verifyStubbedInvocationsAreUsed()


def test_av_error():
    CTX.appveyor = True
    when(subprocess).call(f'appveyor AddMessage "message" -Category Error')
    epab.utils.AV.error('message')
    verifyStubbedInvocationsAreUsed()


def test_av_error_details():
    CTX.appveyor = True
    when(subprocess).call(f'appveyor AddMessage "message" -Category Error -Details "details"')
    epab.utils.AV.error('message', 'details')
    verifyStubbedInvocationsAreUsed()


def test_av_unknown_level():
    expect(subprocess, times=0).call(...)
    with pytest.raises(ValueError):
        epab.utils.AV._out('some level', 'message')


def test_update_build_version():
    when(elib_run).run('appveyor UpdateBuild -Version version')
    epab.utils.AV.update_build_version('version')
    verifyStubbedInvocationsAreUsed()
