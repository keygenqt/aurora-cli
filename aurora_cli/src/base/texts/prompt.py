from enum import Enum


class TextPrompt(Enum):
    @staticmethod
    def emulator_recording_video_loading():
        return 'Press to stop recording'

    @staticmethod
    def select_index():
        return 'Please enter index'
