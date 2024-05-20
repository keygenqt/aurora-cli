from enum import Enum


class TextInfo(Enum):
    @staticmethod
    def command_execute(command: str) -> str:
        return f'<blue>Command execute:</blue> `{command}`'

    @staticmethod
    def emulator_start_locked() -> str:
        return '<blue>The emulator is already running.</blue>'

    @staticmethod
    def emulator_recording_video_start_already() -> str:
        return '<blue>The emulator recording video is already on.</blue>'

    @staticmethod
    def emulator_recording_video_stop_already() -> str:
        return '<blue>The emulator recording video is already off.</blue>'

    @staticmethod
    def shh_download_start(path: str) -> str:
        return f'<blue>Starting file download:</blue> {path}'

    @staticmethod
    def shh_download_progress() -> str:
        return '<blue>File download progress in percentage.</blue>'

    @staticmethod
    def ssh_install_rpm() -> str:
        return '<blue>Starting install RPM package...</blue>'
