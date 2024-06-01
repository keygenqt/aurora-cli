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
from aurora_cli.src.base.utils.output import echo_stdout, OutResult


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
