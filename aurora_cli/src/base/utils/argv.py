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

import sys

from aurora_cli.src.base.utils.cache_settings import CacheSettingsKey, cache_settings_get


def argv_is_api() -> bool:
    if len(sys.argv) >= 2 and 'api' in sys.argv[1]:
        return True
    return False


def argv_is_emulator_recording() -> bool:
    if 'emulator' in sys.argv and 'recording' in sys.argv:
        return True
    return False


def argv_is_verbose() -> bool:
    settings_val = cache_settings_get(CacheSettingsKey.verbose)
    if settings_val and not argv_is_api():
        return settings_val

    if '-v' in sys.argv or '--verbose' in sys.argv:
        return True
    return False


def argv_is_apm() -> bool:
    if '-a' in sys.argv or '--apm' in sys.argv:
        return True
    return False


def argv_is_select() -> bool:
    if '-s' in sys.argv or '--select' in sys.argv:
        return True
    return False


def argv_is_help() -> bool:
    if '--help' in sys.argv:
        return True
    return False


def argv_is_test() -> bool:
    if sys.argv and 'unittest_runner' in sys.argv[0]:
        return True
    return False
