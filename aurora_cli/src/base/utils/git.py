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
from collections.abc import Callable
from pathlib import Path

from git import Repo

from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.git_title import TitleOpCode
from aurora_cli.src.base.utils.output import echo_stdout, OutResultInfo


def git_clone(
        url: str,
        path: Path,
        verbose: bool,
        is_bar: bool = True
):
    bar = AliveBarPercentage()

    def bar_update(title: str, result: int):
        if is_bar:
            bar.update(result, title, 11)
        else:
            echo_stdout(OutResultInfo(TextInfo.git_clone_progress(title), value=result), verbose)

    # @todo success, error, ctrl+c

    _git_clone(url, path, bar_update)


def _git_clone(
        url: str,
        path: Path,
        listen: Callable[[str, int], None]
):
    percents = []

    def _update(op_code: int, cur_count: float, max_count: float, _: str):
        percent = int(cur_count * 100 / max_count)
        if not percent:
            percents.clear()
        if percent not in percents:
            percents.append(percent)
            listen(TitleOpCode.get_title(op_code), percent)

    Repo.clone_from(
        url=url,
        to_path=path,
        progress=_update
    )
