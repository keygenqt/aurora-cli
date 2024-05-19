from enum import Enum


class TextError(Enum):
    @staticmethod
    def emulator_start_error() -> str:
        return '<red>Failed to start the emulator.</red>'

    @staticmethod
    def route_not_found() -> str:
        return '<red>Route not found.</red>'

    @staticmethod
    def emulator_screenshot_error() -> str:
        return '<red>Failed to take screenshot.</red>'

    @staticmethod
    def emulator_recording_video_start_error() -> str:
        return '<red>Failed to activate video recording.</red>'

    @staticmethod
    def emulator_recording_video_stop_error() -> str:
        return '<red>Failed to deactivate video recording.</red>'

    @staticmethod
    def emulator_recording_video_file_not_found() -> str:
        return '<red>Could not find video recording.</red>'

    @staticmethod
    def emulator_recording_video_convert_error() -> str:
        return '<red>Could not convert video recording.</red>'
