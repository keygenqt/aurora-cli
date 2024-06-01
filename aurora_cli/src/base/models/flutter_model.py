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

from aurora_cli.src.base.common.search_features import search_installed_flutter
from aurora_cli.src.base.utils.output import OutResult
from aurora_cli.src.base.utils.prompt import prompt_model_select


@dataclass
class FlutterModel:
    """Class Aurora Platform SDK."""
    flutter: Path
    dart: Path

    @staticmethod
    def get_model_select(select: bool, index: int | None) -> OutResult:
        return prompt_model_select(
            name='flutter',
            models=FlutterModel.get_versions_flutter(),
            select=select,
            index=index
        )

    @staticmethod
    def get_model_by_version(version: str):
        list_index = FlutterModel.get_versions_flutter().index(version)
        path_flutter = FlutterModel.get_tools_flutter()[list_index]
        path_dart = FlutterModel.get_tools_dart()[list_index]
        return FlutterModel(path_flutter, path_dart)

    @staticmethod
    def get_versions_flutter() -> []:
        return FlutterModel._get_lists('versions')

    @staticmethod
    def get_tools_flutter() -> []:
        return FlutterModel._get_lists('flutters')

    @staticmethod
    def get_tools_dart() -> []:
        return FlutterModel._get_lists('darts')

    @staticmethod
    def _get_lists(key: str) -> []:
        result = search_installed_flutter()
        if result.is_error():
            return []
        return search_installed_flutter().value[key]

    def get_tool_flutter(self) -> str:
        return str(self.flutter)

    def get_tool_dart(self) -> str:
        return str(self.dart)
