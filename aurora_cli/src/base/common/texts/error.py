from enum import Enum


class TextError(Enum):
    @staticmethod
    def emulator_start_error():
        return '<red>Failed to start the emulator.</red>'

    @staticmethod
    def route_not_found():
        return '<red>Route not found.</red>'
