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

from aurora_cli.src.base.common.features.search_installed import search_installed_psdk
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.output import OutResult, echo_stdout, OutResultError
from aurora_cli.src.base.utils.prompt import prompt_model_select


@dataclass
class PsdkModel:
    """Class Aurora Platform SDK."""
    tool: Path

    @staticmethod
    def get_model_select(select: bool, index: int | None) -> OutResult:
        return prompt_model_select(
            name='psdk',
            models=PsdkModel.get_versions_psdk(),
            select=select,
            index=index
        )

    @staticmethod
    def get_model_by_version(version: str, verbose: bool):
        try:
            list_index = PsdkModel.get_versions_psdk().index(version)
            path_tool = PsdkModel.get_tools_psdk()[list_index]
            return PsdkModel(Path(path_tool))
        except (Exception,):
            echo_stdout(OutResultError(TextError.psdk_not_found_error()), verbose)
            exit(1)

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
        return search_installed_psdk().value[key]

    def get_tool_path(self) -> str:
        return str(self.tool)
