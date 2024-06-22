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
from typing import Any

from alive_progress import alive_bar

from aurora_cli.src.base.utils.argv import argv_is_test


class AliveBarPercentage:
    def __init__(self) -> None:
        super().__init__()
        self.alive_bar_instance = None

    def stop(self):
        if self.alive_bar_instance:
            self._destroy_bar()

    def update(
            self,
            percentage: int,
            title: Any = None,
            title_length: Any = None,
    ):
        if not argv_is_test():
            if not self.alive_bar_instance:
                self._dispatch_bar(title, title_length)
            self.bar(percentage * 0.01)
            if percentage == 100:
                self._destroy_bar()

    def _dispatch_bar(
            self,
            title: Any = None,
            title_length: Any = None
    ):
        self.alive_bar_instance = alive_bar(
            manual=True,
            title=title if title else '',
            stats='({eta})',
            title_length=title_length if title_length else 0,
        )
        self.bar = self.alive_bar_instance.__enter__()

    def _destroy_bar(self):
        if self.alive_bar_instance:
            self.alive_bar_instance.__exit__(None, None, None)
            self.alive_bar_instance = None
