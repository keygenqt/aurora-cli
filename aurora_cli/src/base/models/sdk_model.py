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

from aurora_cli.src.base.common.features.search_installed import search_installed_sdk
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError


@dataclass
class SdkModel:
    """Class Aurora SDK."""
    tool: Path

    @staticmethod
    def get_model():
        versions = SdkModel.get_versions_sdk()
        if not versions:
            echo_stdout(OutResultError(TextError.sdk_not_found_error()))
            app_exit()
        return SdkModel.get_model_by_version(versions[0])

    @staticmethod
    def get_model_by_version(version: str):
        try:
            list_index = SdkModel.get_versions_sdk().index(version)
            path_tool = SdkModel.get_tools_sdk()[list_index]
            return SdkModel(Path(path_tool))
        except (Exception,):
            echo_stdout(OutResultError(TextError.sdk_not_found_error(version)))
            app_exit()

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
