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
from aurora_cli.src.base.common.request_features import get_versions_sdk
from aurora_cli.src.base.common.search_features import search_installed_sdk
from aurora_cli.src.base.models.sdk_model import SdkModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultError
from aurora_cli.src.base.utils.shell import shell_exec_app


def sdk_available_api(verbose: bool):
    versions = get_versions_sdk()
    if versions.is_error():
        return versions
    versions = versions.message.split('\n')
    echo_stdout(OutResult(
        message=versions[0],
        value=versions[1:] if len(versions) > 1 else []
    ), verbose)


def sdk_installed_api(verbose: bool):
    versions = search_installed_sdk()
    if versions.is_error():
        return versions
    versions = versions.message.split('\n')
    echo_stdout(OutResult(
        message=versions[0],
        value=versions[1:] if len(versions) > 1 else []
    ), verbose)


def sdk_tool_api(version: str, verbose: bool):
    model = SdkModel.get_model_by_version(version)
    if not model:
        echo_stdout(OutResultError(TextError.sdk_not_found_error()), verbose)
        exit(0)
    tool = model.get_tool_path()
    if shell_exec_app(tool):
        echo_stdout(OutResult(TextSuccess.shell_run_app_success(tool.name)), verbose)
    else:
        echo_stdout(OutResultError(TextError.shell_run_app_error(tool.name)), verbose)
