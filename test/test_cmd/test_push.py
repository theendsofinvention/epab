# coding=utf-8

from mockito import mock, verify, when

import epab.cmd
import epab.linters
import epab.utils
from epab.cmd._push import _push
from epab.core import CTX


def test_push():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    when(CTX.repo).push()
    context = mock()
    _push(context)
    verify(context).invoke(epab.linters.lint, amend=True)
    verify(context).invoke(epab.cmd.pytest, long=True, exitfirst=True, failed_first=True)
    verify(context).invoke(epab.cmd.reqs, amend=True)
    verify(context).invoke(epab.cmd.chglog, amend=True)
    verify(CTX.repo).push()
