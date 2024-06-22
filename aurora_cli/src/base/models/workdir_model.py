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

from aurora_cli.src.base.utils.path import path_convert_relative


@dataclass
class WorkdirModel:
    """Class path workdir for search sdk & psdk."""
    path: Path

    @staticmethod
    def get_model(path: Any):
        if not path:
            path = '~/'
        return WorkdirModel(path_convert_relative(path))

    @staticmethod
    @click.pass_context
    def get_workdir(ctx: {}) -> Path:
        return WorkdirModel.get_model(ctx.obj.get_workdir()).path
