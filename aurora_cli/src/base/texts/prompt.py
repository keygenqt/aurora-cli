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

from enum import Enum

from aurora_cli.src.base.localization.localization import localization


class TextPrompt(Enum):
    @staticmethod
    @localization
    def emulator_recording_video_loading():
        return 'Press to stop recording'

    @staticmethod
    @localization
    def select_index():
        return 'Please enter index'

    @staticmethod
    @localization
    def select_continue():
        return 'Do you want to continue?'

    @staticmethod
    @localization
    def is_ready():
        return 'Are you ready to continue?'


