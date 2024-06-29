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

import click

from aurora_cli.src.base.common.features.request_version import (
    request_versions_flutter,
    request_versions_sdk,
    request_versions_psdk
)
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.prompt import TextPrompt
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.cache_settings import cache_settings_get, CacheSettingsKey
from aurora_cli.src.base.utils.cache_values import cache_values_save, cache_values_get
from aurora_cli.src.base.utils.output import OutResultError, OutResult, echo_stdout


def prompt_flutter_select_version(select: bool) -> Any:
    versions = request_versions_flutter()
    if versions.is_error():
        echo_stdout(versions)
        app_exit()
    prompt_result = prompt_model_select('flutter', versions.value, select, None)
    if prompt_result.is_error():
        echo_stdout(prompt_result)
        app_exit()
    return prompt_result.value


def prompt_psdk_select_version(select: bool) -> Any:
    versions = request_versions_sdk()
    if versions.is_error():
        echo_stdout(versions)
        app_exit()
    prompt_result = prompt_model_select('psdk', versions.value, select, None)
    if prompt_result.is_error():
        echo_stdout(prompt_result)
        app_exit()
    return prompt_result.value


def prompt_sdk_select_version(select: bool) -> Any:
    versions = request_versions_psdk()
    if versions.is_error():
        echo_stdout(versions)
        app_exit()
    prompt_result = prompt_model_select('sdk', versions.value, select, None)
    if prompt_result.is_error():
        echo_stdout(prompt_result)
        app_exit()
    return prompt_result.value


def prompt_model_select(
        name: str,
        models: [],
        select: bool,
        index: Any,
) -> OutResult:
    def not_has_index(i: int, arr: []) -> bool:
        return i < 0 or len(arr) <= i

    # At the same time index and select
    if select and index is not None:
        return OutResultError(TextError.index_and_select_at_the_same_time())
    # If empty
    if len(models) == 0:
        return OutResultError(TextError.config_value_empty_error())
    # If select index
    if index is not None:
        if not_has_index(index - 1, models):
            return OutResultError(TextError.index_error())
        return OutResult(value=models[index - 1])
    # If not prompt select fist
    if not select:
        index_default = _get_select_default(name)
        if not index_default or not_has_index(index_default - 1, models):
            return OutResult(value=models[0])
        else:
            return OutResult(value=models[index_default - 1])
    # If one item
    if not select and len(models) == 1:
        return OutResult(value=models[0])
    # Prompt
    echo_stdout(TextInfo.select_array_out(name, models))
    index = click.prompt(TextPrompt.select_index(), type=int)
    # Check index
    if not_has_index(index - 1, models):
        return OutResultError(TextError.index_error())
    # Save select
    _save_sate_select(name, index)
    # Result
    return OutResult(value=models[index - 1])


def _save_sate_select(name: str, index: int):
    settings_val = cache_settings_get(CacheSettingsKey.select)
    if settings_val:
        cache_values_save(name, index)


def _get_select_default(name: str) -> Any:
    settings_val = cache_settings_get(CacheSettingsKey.select)
    if settings_val:
        return cache_values_get(name)
    return None
