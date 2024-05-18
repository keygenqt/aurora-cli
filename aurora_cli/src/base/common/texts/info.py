from enum import Enum


class TextInfo(Enum):
    @staticmethod
    def command_execute(command: str) -> str:
        return f'<blue>Command execute:</blue> `{command}`'

    @staticmethod
    def emulator_start_locked() -> str:
        return '<blue>The emulator is already running.</blue>'
