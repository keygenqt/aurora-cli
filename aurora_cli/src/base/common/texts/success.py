from enum import Enum


class TextSuccess(Enum):
    @staticmethod
    def emulator_start_success():
        return '<green>Emulator started successfully.</green>'
