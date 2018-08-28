# coding=utf-8

import elib_run
from mockito import verifyStubbedInvocationsAreUsed, when

import epab.utils
from epab.cmd import _compile_qt
from epab.core import config


def test_compile_qt_resources():
    when(epab.utils).ensure_exe('pyrcc5').thenReturn(True)
    config.QT_RES_SRC.default = 'src'
    config.QT_RES_TGT.default = 'tgt'
    when(elib_run).run(f'pyrcc5 {config.QT_RES_SRC()} -o {config.QT_RES_TGT()}')
    _compile_qt._compile_qt_resources()
    verifyStubbedInvocationsAreUsed()
