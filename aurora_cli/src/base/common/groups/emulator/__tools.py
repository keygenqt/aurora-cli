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
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_stdout, OutResultInfo


def emulator_tool_check_is_not_run(model: EmulatorModel):
    if not model.is_on:
        echo_stdout(OutResultInfo(TextError.emulator_not_found_running()))
        app_exit()
