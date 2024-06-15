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

from aurora_cli.src.base.models.emulator_model import EmulatorModel


def cli_emulator_tool_select_model(is_root: bool = False) -> EmulatorModel:
    if is_root:
        return EmulatorModel.get_model_root()
    else:
        return EmulatorModel.get_model_user()
