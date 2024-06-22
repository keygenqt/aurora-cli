"""
Copyright 2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import signal
from typing import Callable

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
