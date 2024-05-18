from enum import Enum


class TextSuccess(Enum):
    @staticmethod
    def emulator_start_success():
        return '<green>Emulator started successfully.</green>'

    @staticmethod
    def emulator_screenshot_success(path: str):
        return '<green>Screenshot taken successfully:</green> {}'.format(path)
