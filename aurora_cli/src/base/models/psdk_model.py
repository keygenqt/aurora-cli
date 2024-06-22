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

from aurora_cli.src.base.common.features.search_installed import search_installed_psdk
from aurora_cli.src.base.common.features.shell_features import shell_psdk_targets
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import OutResult, echo_stdout, OutResultError, OutResultInfo
from aurora_cli.src.base.utils.prompt import prompt_model_select
from aurora_cli.src.base.utils.tests import tests_exit


@dataclass
class PsdkModel:
    """Class Aurora Platform SDK."""
    tool: Path
    version: str

    @staticmethod
    def get_model_select(
            select: bool,
            index: Any,
    ) -> OutResult:
        versions = PsdkModel.get_versions_psdk()
        if not versions:
            return OutResultError(TextError.psdk_not_found_error())
        return prompt_model_select(
            name='psdk',
            models=versions,
            select=select,
            index=index,
        )

    def get_model_targets_select(self) -> OutResult:
        targets = self.get_targets_psdk()
        if not targets:
            return OutResultInfo(TextInfo.psdk_targets_empty(self.get_version()))
        return prompt_model_select(
            name='target',
            models=targets,
            select=True,
            index=None,
        )

    @staticmethod
    def get_model_by_version(version: str):
        tests_exit()
        try:
            list_index = PsdkModel.get_versions_psdk().index(version)
            path_tool = PsdkModel.get_tools_psdk()[list_index]
            return PsdkModel(Path(path_tool), version)
        except (Exception,):
            echo_stdout(OutResultError(TextError.psdk_not_found_error(version)))
            app_exit()

    @staticmethod
    def get_versions_psdk() -> []:
        return PsdkModel._get_lists('versions')

    @staticmethod
    def get_tools_psdk() -> []:
        return PsdkModel._get_lists('tools')

    @staticmethod
    def _get_lists(key: str) -> []:
        result = search_installed_psdk()
        if result.is_error():
            return []
        return result.value[key]

    def get_targets_psdk(self) -> []:
        result = shell_psdk_targets(self.get_tool_path(), self.get_version())
        if not result.is_success():
            return []
        return result.value

    def get_version(self) -> str:
        return str(self.version)

    def get_tool_path(self) -> str:
        return str(self.tool)

    def get_psdk_dir(self) -> str:
        return str(self.tool.parent)

    def get_path(self) -> str:
        return str(self.tool.parent.parent.parent)
