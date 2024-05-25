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

from aurora_cli.src.base.localization.ru import ru_localization


def localization(func):
    def wrapped(*args, **kwargs) -> str:
        @click.pass_context
        def wrapped_context(ctx: {}):
            if ctx.obj.get_localization() == 'ru':
                return ru_localization(func.__name__, *args, **kwargs)

        value = wrapped_context()
        if value:
            return value
        return func(*args, **kwargs)

    return wrapped
