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
from aurora_cli.src.base.output import echo_stdout_json
from aurora_cli.src.common.emulator.features import emulator_start, emulator_screenshot, emulator_record_start, \
    emulator_record_stop, emulator_record_is_on


def command_start(verbose: bool):
    """Start emulator."""
    echo_stdout_json(emulator_start(), verbose)


def command_screenshot(verbose: bool):
    """Emulator take screenshot."""
    echo_stdout_json(emulator_screenshot(), verbose)


def command_recording_video_start(verbose: bool):
    """Start recording video from emulator."""
    echo_stdout_json(emulator_record_start(), verbose)


def command_recording_video_stop(verbose: bool):
    """Stop recording video from emulator."""
    echo_stdout_json(emulator_record_stop(), verbose)


def command_recording_video_is_on(verbose: bool):
    """Check recording video from emulator."""
    echo_stdout_json(emulator_record_is_on(), verbose)
