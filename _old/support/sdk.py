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
import os
from pathlib import Path

from aurora_cli.src.support.helper import get_first_or_none, check_home_folder
from aurora_cli.src.support.output import echo_stderr
from aurora_cli.src.support.texts import AppTexts


# Get path Aurora SDK
def find_folder_sdk(workdir: Path) -> Path:
    path = _find_folder_sdks(workdir, Path('sdk-release'))
    if not path:
        echo_stderr(AppTexts.sdk_not_found())
        exit(0)
    return workdir / str(path)


# Get path Aurora Platform SDK
def find_folder_psdk(workdir: Path) -> Path:
    path = _find_folder_sdks(workdir, Path('sdks') / 'aurora_psdk' / 'sdk-chroot')
    if not path:
        echo_stderr(AppTexts.psdk_not_found())
        exit(0)
    return workdir / str(path)


# Get installed sdk or psdk
def _find_folder_sdks(workdir: Path, contains_file_path: Path):
    return get_first_or_none(
        [d for d in os.listdir(workdir) if check_home_folder(workdir, d, 'Aurora', str(contains_file_path))]
    )
