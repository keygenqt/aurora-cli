import signal
from collections.abc import Callable

from aurora_cli.src.base.localization.localization import localization_abort


def abort_text_start():
    localization_abort('Aborted! Closing...')


def abort_text_end():
    localization_abort('Goodbye 👋')


def abort_catch(listen: Callable[[], None]):
    def signal_handler(s, f):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        listen()

    signal.signal(signal.SIGINT, signal_handler)
