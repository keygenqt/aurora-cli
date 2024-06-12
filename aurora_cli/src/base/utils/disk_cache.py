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

from diskcache import Cache

from aurora_cli.src.base.constants.config import APP_FOLDER
from aurora_cli.src.base.utils.path import path_convert_relative


# Default cache = 12 hours
# App has flag --clear-cache for force clear
def disk_cache(expire=43200):
    def decorator(func):
        def wrapper(*args, **kwargs) -> str:
            def save(data):
                with Cache(APP_FOLDER) as reference:
                    reference.set(func.__name__, data, expire=expire)

            def get():
                with Cache(APP_FOLDER) as reference:
                    return reference.get(func.__name__)

            cache = get()
            if cache:
                return cache
            orig_value = func(*args, **kwargs)
            save(orig_value)
            return orig_value

        return wrapper

    return decorator


def disk_cache_clear():
    (path_convert_relative(APP_FOLDER) / 'cache.db').unlink(missing_ok=True)
