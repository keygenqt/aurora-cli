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


# Get path Aurora SDK
def find_folder_sdk() -> Path:
    return Path.home() / _find_folder_sdks(Path('sdk-release'))


# Get path Aurora Platform SDK
def find_folder_psdk() -> Path:
    return Path.home() / _find_folder_sdks(Path('sdks') / 'aurora_psdk' / 'sdk-chroot')


# Get installed sdk or psdk
def _find_folder_sdks(contains_file_path: Path) -> []:
    return get_first_or_none(
        [d for d in os.listdir(Path.home()) if check_home_folder(d, 'Aurora', str(contains_file_path))]
    )
