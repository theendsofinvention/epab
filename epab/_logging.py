# coding=utf-8
"""
Logging related handlers & formatters
"""
import logging

import click

import epab.utils
from epab.core import CTX

LOGGER = logging.getLogger('EPAB')

_LOGGING_CONSOLE_FORMAT = '%(relativeCreated)10d ms ' \
                          '%(levelname)8s ' \
                          '%(message)s'


class _ClickHandler(logging.StreamHandler):

    def emit(self, record: logging.LogRecord):
        level_to_color = {
            logging.DEBUG: ('white', 'black'),
            logging.INFO: ('cyan', 'black'),
            logging.WARNING: ('yellow', 'black'),
            logging.ERROR: ('red', 'black'),
            logging.CRITICAL: ('white', 'red'),
        }

        text = self.format(record)
        level = record.levelno
        foreground, background = level_to_color[level]
        click.secho(text, fg=foreground, bg=background)


class _AVHandler(logging.Handler):

    def emit(self, record: logging.LogRecord):
        av_func = {
            logging.DEBUG: epab.utils.AV.info,
            logging.INFO: epab.utils.AV.info,
            logging.WARNING: epab.utils.AV.error,
            logging.ERROR: epab.utils.AV.error,
            logging.CRITICAL: epab.utils.AV.error,
        }
        if CTX.appveyor:
            av_func[record.levelno](record.msg % record.args)


def _setup_logging():
    formatter = logging.Formatter(fmt=_LOGGING_CONSOLE_FORMAT)
    click_handler = _ClickHandler()
    click_handler.setLevel(logging.DEBUG)
    av_handler = _AVHandler()
    av_handler.setLevel(logging.INFO)
    for handler in (click_handler,
                    av_handler,
                    ):
        handler.setFormatter(formatter)

    elib_run_logger = logging.getLogger('elib_run')
    elib_run_process_logger = logging.getLogger('elib_run.process')
    elib_run_process_logger.propagate = False

    for logger in (LOGGER,
                   elib_run_logger,
                   elib_run_process_logger
                   ):
        logger.setLevel(logging.DEBUG)
        logger.addHandler(click_handler)
        logger.addHandler(av_handler)
