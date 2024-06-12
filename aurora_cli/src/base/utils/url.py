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

from aurora_cli.src.base.constants.url import (
    URL_AURORA_REPO_SDK,
    URL_AURORA_REPO_PSDK,
    URL_FLUTTER_GIT
)


def get_url_git_flutter() -> str:
    return URL_FLUTTER_GIT


def get_url_version_psdk(version: str) -> str:
    return URL_AURORA_REPO_PSDK.format(version=version)


def get_url_version_sdk(version: str) -> str:
    return URL_AURORA_REPO_SDK.format(version=version)
