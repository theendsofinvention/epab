# coding=utf-8

from mockito import verifyStubbedInvocationsAreUsed, when

import epab.utils
from epab.cmd import _compile_qt
from epab.core import CONFIG


def test_compile_qt_resources():
    when(epab.utils).ensure_exe('pyrcc5').thenReturn(True)
    CONFIG.qt__res_src = 'src'
    CONFIG.qt__res_tgt = 'tgt'
    when(epab.utils).run(f'pyrcc5 {CONFIG.qt__res_src} -o {CONFIG.qt__res_tgt}')
    _compile_qt._compile_qt_resources()
    verifyStubbedInvocationsAreUsed()
