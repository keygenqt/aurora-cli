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
import os
import traceback

import click

from aurora_cli.src.base.utils.argv import argv_is_verbose


def app_crash_out(e: Exception):
    print(click.style('An unexpected error occurred in the application.', fg='red'))
    if argv_is_verbose():
        traceback.print_exception(e)


def app_language() -> str:
    return 'ru'
    if 'ru_RU' in os.getenv("LANG"):
        return 'ru'
    else:
        return 'en'
