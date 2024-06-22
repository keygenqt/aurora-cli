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


class TextPromptRu(Enum):
    @staticmethod
    def emulator_recording_video_loading():
        return 'Нажмите, чтобы остановить запись'

    @staticmethod
    def select_index():
        return 'Пожалуйста, введите индекс'

    @staticmethod
    def select_continue():
        return 'Вы хотите продолжить?'

    @staticmethod
    def is_ready():
        return 'Вы готовы продолжить?'
