# coding=utf-8
import elib_run
import pytest
from mockito import verifyStubbedInvocationsAreUsed, when

import epab.utils
from epab.core import CTX


def test_info():
    when(epab.utils).info('message')
    epab.utils.AV.info('message')
    verifyStubbedInvocationsAreUsed()


def test_info_details():
    when(epab.utils).info('message: details')
    epab.utils.AV.info('message', 'details')
    verifyStubbedInvocationsAreUsed()


def test_error():
    when(epab.utils).error('message: details')
    epab.utils.AV.error('message', 'details')
    verifyStubbedInvocationsAreUsed()


def test_av_info():
    CTX.appveyor = True
    when(elib_run).run(f'appveyor AddMessage "message" -Category Information', mute=True)
    epab.utils.AV.info('message')
    verifyStubbedInvocationsAreUsed()


def test_av_info_details():
    CTX.appveyor = True
    when(elib_run).run(f'appveyor AddMessage "message" -Category Information -Details "details"', mute=True)
    epab.utils.AV.info('message', 'details')
    verifyStubbedInvocationsAreUsed()


def test_av_error():
    CTX.appveyor = True
    when(elib_run).run(f'appveyor AddMessage "message" -Category Error', mute=True)
    epab.utils.AV.error('message')
    verifyStubbedInvocationsAreUsed()


def test_av_error_details():
    CTX.appveyor = True
    when(elib_run).run(f'appveyor AddMessage "message" -Category Error -Details "details"', mute=True)
    epab.utils.AV.error('message', 'details')
    verifyStubbedInvocationsAreUsed()


def test_av_unknown_level():
    with pytest.raises(ValueError):
        epab.utils.AV._out('some level', 'message')


def test_update_build_version():
    when(elib_run).run('appveyor UpdateBuild -Version version')
    epab.utils.AV.update_build_version('version')
    verifyStubbedInvocationsAreUsed()
