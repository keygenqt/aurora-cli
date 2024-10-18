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

from pathlib import Path
from typing import Callable

import click
from git import Repo, GitCommandError

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.app import app_abort_handler
from aurora_cli.src.base.utils.argv import argv_is_api
from aurora_cli.src.base.utils.git_title import TitleOpCode
from aurora_cli.src.base.utils.output import echo_stdout, OutResultInfo, OutResultError, OutResult


def git_clone(
        url: str,
        path: Path,
        is_bar: bool = True
) -> Repo:
    bar = AliveBarPercentage()

    try:
        app_abort_handler(lambda: bar.stop())

        def bar_update(title: str, result: int):
            if is_bar:
                bar.update(result, title, 11)
            else:
                if argv_is_api():
                    echo_stdout(OutResultInfo(title, value=result))
                else:
                    echo_stdout(OutResultInfo(TextInfo.git_clone_progress(title), value=result))

        echo_stdout(OutResultInfo(TextInfo.git_clone_start(url)))

        repo = _git_clone(url, path, bar_update)
        echo_stdout(OutResultInfo(TextSuccess.git_clone_success()))
        return repo
    except GitCommandError as e:
        bar.stop()
        if 'code(-2)' in str(e):
            raise click.exceptions.Abort
        else:
            echo_stdout(OutResultError(TextError.git_clone_error()))
    except (Exception,):
        echo_stdout(OutResultError(TextError.git_clone_error()))


def _git_clone(
        url: str,
        path: Path,
        listen: Callable[[str, int], None]
) -> Repo:
    percents = []

    def _update(op_code: int, cur_count: float, max_count: float, _: str):
        percent = int(cur_count * 100 / max_count)
        if not percent:
            percents.clear()
        if percent not in percents:
            percents.append(percent)
            listen(TitleOpCode.get_title(op_code), percent)

    return Repo.clone_from(
        url=url,
        to_path=path,
        progress=_update
    )
