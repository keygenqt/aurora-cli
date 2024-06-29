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

from diskcache import Cache

from aurora_cli.src.base.constants.config import APP_FOLDER

_cache_func_path = Path(APP_FOLDER) / 'cache_func'
_cache_func_cache = Cache(str(_cache_func_path))


# Default cache = 12 hours
# App has flag --clear-cache for force clear
def cache_func(expire=43200):
    def decorator(func):
        def wrapper(*args, **kwargs) -> str:
            def save(data):
                _cache_func_cache.set(func.__name__, data, expire=expire)

            def get():
                return _cache_func_cache.get(func.__name__)

            cache = get()
            if cache:
                return cache
            orig_value = func(*args, **kwargs)
            save(orig_value)
            return orig_value

        return wrapper

    return decorator


def cache_func_clear():
    _cache_func_cache.clear()
