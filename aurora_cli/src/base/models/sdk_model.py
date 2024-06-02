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

from aurora_cli.src.base.common.search_features import search_installed_sdk
from aurora_cli.src.base.utils.output import OutResult
from aurora_cli.src.base.utils.prompt import prompt_model_select


@dataclass
class SdkModel:
    """Class Aurora SDK."""
    tool: Path

    @staticmethod
    def get_model_select(select: bool, index: int | None) -> OutResult:
        return prompt_model_select(
            name='sdk',
            models=SdkModel.get_versions_sdk(),
            select=select,
            index=index
        )

    @staticmethod
    def get_model_by_version(version: str):
        try:
            list_index = SdkModel.get_versions_sdk().index(version)
            path_tool = SdkModel.get_tools_sdk()[list_index]
            return SdkModel(path_tool)
        except (Exception,):
            return None

    @staticmethod
    def get_versions_sdk() -> []:
        return SdkModel._get_lists('versions')

    @staticmethod
    def get_tools_sdk() -> []:
        return SdkModel._get_lists('tools')

    @staticmethod
    def _get_lists(key: str) -> []:
        result = search_installed_sdk()
        if result.is_error():
            return []
        return search_installed_sdk().value[key]

    def get_tool_path(self) -> Path:
        return self.tool
