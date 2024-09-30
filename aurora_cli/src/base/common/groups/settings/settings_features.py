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
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.cache_settings import (
    CacheSettingsKey,
    cache_settings_save,
    cache_settings_clear,
    cache_settings_get
)
from aurora_cli.src.base.utils.output import echo_stdout, OutResult


def settings_list_common():
    settings_list = {}
    for enum in CacheSettingsKey:
        value = cache_settings_get(enum)
        if value is None:
            settings_list[enum.value] = TextInfo.settings_item_empty()
        else:
            settings_list[enum.value] = str(value).lower()

    echo_stdout(OutResult(TextInfo.settings_list(settings_list), value=settings_list))


def settings_clear_common():
    cache_settings_clear()
    echo_stdout(OutResult(TextSuccess.settings_clear()))


def settings_localization_common(language: str):
    cache_settings_save(CacheSettingsKey.language, language)
    echo_stdout(OutResult(TextSuccess.settings_localization_update()))


def settings_verbose_common(enable: bool):
    cache_settings_save(CacheSettingsKey.verbose, enable)
    if enable:
        echo_stdout(OutResult(TextSuccess.settings_verbose_enable()))
    else:
        echo_stdout(OutResult(TextSuccess.settings_verbose_disable()))


def settings_select_common(enable: bool):
    cache_settings_save(CacheSettingsKey.select, enable)
    if enable:
        echo_stdout(OutResult(TextSuccess.settings_select_enable()))
    else:
        echo_stdout(OutResult(TextSuccess.settings_select_disable()))


def settings_hint_common(enable: bool):
    cache_settings_save(CacheSettingsKey.hint, enable)
    if enable:
        echo_stdout(OutResult(TextSuccess.settings_hint_enable()))
    else:
        echo_stdout(OutResult(TextSuccess.settings_hint_disable()))
