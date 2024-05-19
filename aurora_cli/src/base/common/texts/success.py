from enum import Enum


class TextSuccess(Enum):
    @staticmethod
    def emulator_start_success() -> str:
        return '<green>Emulator started successfully.</green>'

    @staticmethod
    def emulator_screenshot_success(path: str) -> str:
        return '<green>Screenshot taken successfully:</green> {}'.format(path)

    @staticmethod
    def emulator_recording_video_start() -> str:
        return '<green>Video recording activated.</green>'

    @staticmethod
    def emulator_recording_video_stop() -> str:
        return '<green>Video recording is deactivated.</green>'

    @staticmethod
    def emulator_recording_video_convert(path: str) -> str:
        return '<green>Video record convert successfully:</green> {}'.format(path)

    @staticmethod
    def emulator_exec_command_success(execute: str, stdout: str = None, stderr: str = None) -> str:
        stdout = f'\n{stdout}' if stdout else ''
        stderr = f'\n{stderr}' if stderr else ''
        return f'<green>The command was executed successfully:</green> `{execute}`{stdout}{stderr}'
