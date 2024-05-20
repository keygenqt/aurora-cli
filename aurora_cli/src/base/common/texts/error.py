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

    @staticmethod
    def ssh_connect_emulator_error() -> str:
        return '<red>Error connecting to emulator via SSH.</red>'

    @staticmethod
    def ssh_connect_device_error() -> str:
        return '<red>Error connecting to device via SSH.</red>'

    @staticmethod
    def ssh_run_application_error(package: str) -> str:
        return f'<red>An error occurred while starting the application:</red> {package}'

    @staticmethod
    def ssh_upload_error() -> str:
        return '<red>Failed to upload files.</red>'

    @staticmethod
    def ssh_install_rpm_error() -> str:
        return '<red>Error installing RPM package.</red>'

    @staticmethod
    def ssh_remove_rpm_error() -> str:
        return '<red>An error occurred while deleting the package.</red>'
