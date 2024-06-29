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
from typing import Any

from diskcache import Cache

from aurora_cli.src.base.constants.config import APP_FOLDER

_cache_values_path = Path(APP_FOLDER) / 'cache_values'
_cache_values_cache = Cache(str(_cache_values_path))


def cache_values_save(key: str, value: Any):
    _cache_values_cache.set(key, value)


def cache_values_get(key: str) -> Any:
    return _cache_values_cache.get(key)


def cache_values_cache_clear():
    _cache_values_cache.clear()
