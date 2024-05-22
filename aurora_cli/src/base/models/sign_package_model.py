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

import click


# @todo
@dataclass
class SignPackageModel:
    """Class device."""
    name: str
    key: Path
    cert: Path

    @staticmethod
    def get_model(name: str, key: Path, cert: Path):
        return SignPackageModel(name, key, cert)

    @staticmethod
    def get_model_select(select: bool, index: int):
        devices = SignPackageModel.get_lists_keys()
        print(devices)
        return None

    # @todo
    @staticmethod
    @click.pass_context
    def get_lists_keys(ctx: {}) -> []:
        return ctx.obj.get_keys()
