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

import click

from aurora_cli.src.base.common.texts.prompt import TextPrompt
from aurora_cli.src.base.output import echo_stdout
from aurora_cli.src.common.emulator.features import emulator_start, emulator_screenshot, emulator_record_start, \
    emulator_record_stop


@click.group(name='emulator')
def group_emulator():
    """Working with the emulator virtualbox."""
    pass


@group_emulator.command(name='start')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def command_start(verbose: bool):
    """Start emulator."""
    echo_stdout(emulator_start(), verbose)


@group_emulator.command(name='screenshot')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def command_screenshot(verbose: bool):
    """Emulator take screenshot."""
    echo_stdout(emulator_screenshot(), verbose)


@group_emulator.command(name='recording')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def command_recording_video(verbose: bool):
    """Recording video from emulator."""
    # Start record
    result = emulator_record_start()
    echo_stdout(result, verbose)
    if result.is_error():
        exit(1)

    # Loading record
    click.prompt(
        text=TextPrompt.emulator_recording_video_loading(),
        prompt_suffix='',
        default='Enter',
        hide_input=True
    )

    # Stop with save record
    echo_stdout(emulator_record_stop(), verbose)
