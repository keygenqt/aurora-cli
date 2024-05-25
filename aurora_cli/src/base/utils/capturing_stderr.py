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
import atexit
import io
import sys
from typing import Callable


class CapturingStderr:

    def __init__(self, callback: Callable[[str], None], ):
        self.callback = callback
        atexit.register(self.exit_handler)

    def __enter__(self):
        self._stderr = sys.stderr
        sys.stderr = self._stringio = io.StringIO()
        return self

    def __exit__(self, *args):
        self.out = '\n'.join(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stderr = self._stderr

    def exit_handler(self):
        self.callback(self.out)
