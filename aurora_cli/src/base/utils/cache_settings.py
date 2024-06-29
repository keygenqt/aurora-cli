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
from enum import Enum
from pathlib import Path
from typing import Any

from diskcache import Cache

from aurora_cli.src.base.constants.config import APP_FOLDER

_cache_settings_path = Path(APP_FOLDER) / 'cache_settings'
_cache_settings_cache = Cache(str(_cache_settings_path))


class CacheSettingsKey(Enum):
    __order__ = 'language verbose select hint'
    language = 'language'
    verbose = 'verbose'
    select = 'select'
    hint = 'hint'


def cache_settings_save(key: CacheSettingsKey, value: Any):
    _cache_settings_cache.set(key, value)


def cache_settings_get(key: CacheSettingsKey) -> Any:
    return _cache_settings_cache.get(key)


def cache_settings_clear():
    _cache_settings_cache.clear()
