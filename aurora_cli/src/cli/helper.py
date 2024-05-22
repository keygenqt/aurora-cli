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

import click

from aurora_cli.src.base.output import OutResultError, OutResult
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.prompt import TextPrompt


def model_select(
        models: [],
        select: bool,
        index: int | None
) -> OutResult:
    def has_index(i: int, arr: []) -> bool:
        return i < 0 or len(arr) <= i

    # At the same time index and select
    if select and index is not None:
        return OutResultError(TextError.index_and_select_at_the_same_time())
    # If empty
    if len(models) == 0:
        return OutResultError(TextError.validate_config_devices_not_found())
    # If select index
    if index is not None:
        if has_index(index - 1, models):
            return OutResultError(TextError.index_error())
        return OutResult(value=models[index - 1])
    # If not prompt select fist
    if not select:
        return OutResult(value=models[0])
    # Prompt
    index = click.prompt(TextPrompt.select_index(), type=int)
    # Check index
    if has_index(index - 1, models):
        return OutResultError(TextError.index_error())
    # Result
    return OutResult(value=models[index - 1])
