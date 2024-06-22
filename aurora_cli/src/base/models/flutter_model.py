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

from aurora_cli.src.base.common.features.search_installed import search_installed_flutter
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import OutResult, echo_stdout, OutResultError
from aurora_cli.src.base.utils.prompt import prompt_model_select
from aurora_cli.src.base.utils.tests import tests_exit


@dataclass
class FlutterModel:
    """Class Aurora Platform SDK."""
    version: str
    flutter: Path
    dart: Path

    @staticmethod
    def get_model_select(
            select: bool,
            index: Any,
    ) -> OutResult:
        versions = FlutterModel.get_versions_flutter()
        if not versions:
            return OutResultError(TextError.flutter_not_found_error())
        return prompt_model_select(
            name='flutter',
            models=versions,
            select=select,
            index=index,
        )

    @staticmethod
    def get_model_by_version(version: str):
        tests_exit()
        try:
            list_index = FlutterModel.get_versions_flutter().index(version)
            path_dart = FlutterModel.get_tools_dart()[list_index]
            path_flutter = FlutterModel.get_tools_flutter()[list_index]
            return FlutterModel(version, Path(path_flutter), Path(path_dart))
        except (Exception,):
            echo_stdout(OutResultError(TextError.flutter_not_found_error(version)))
            app_exit()

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

    def get_path(self) -> str:
        return str(self.flutter.parent.parent)

    def get_version(self) -> str:
        return self.version

    def get_tool_flutter(self) -> str:
        return str(self.flutter)

    def get_tool_dart(self) -> str:
        return str(self.dart)
