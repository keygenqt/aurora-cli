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

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import click

from aurora_cli.src.base.utils.output import OutResult
from aurora_cli.src.base.utils.prompt import prompt_model_select


@dataclass
class SignModel:
    """Class sign keys."""
    name: str
    key: Path
    cert: Path

    @staticmethod
    def get_model_select(
            select: bool,
            index: Any,
    ) -> OutResult:
        return prompt_model_select(
            name='keys',
            models=[model.name for model in SignModel.get_lists_keys()],
            select=select,
            index=index,
        )

    @staticmethod
    def get_model(
            name: str,
            key: Path,
            cert: Path
    ):
        return SignModel(name, key, cert)

    @staticmethod
    def get_model_by_name(name: Any):
        if not name:
            return None
        try:
            models = SignModel.get_lists_keys()
            list_index = [model.name for model in SignModel.get_lists_keys()].index(name)
            return models[list_index]
        except (Exception,):
            return None

    @staticmethod
    @click.pass_context
    def get_lists_keys(ctx: {}) -> []:
        return ctx.obj.get_keys()
