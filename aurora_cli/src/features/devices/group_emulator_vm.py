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
import shutil
import subprocess
from pathlib import Path

import click

from aurora_cli.src.support.dependency_required import check_dependency_ffmpeg
from aurora_cli.src.support.helper import gen_file_name, get_path_file
from aurora_cli.src.support.output import VerboseType, echo_stdout, echo_stderr
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.vbox import vm_search_emulator_aurora, vb_manage_command, vm_check_is_run


@click.group(name='start', invoke_without_command=True)
@click.pass_context
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def emulator_start(ctx: {}, verbose: bool):
    """Start emulator."""

    emulator_name = vm_search_emulator_aurora(VerboseType.none)

    if vm_check_is_run(emulator_name):
        echo_stdout(AppTexts.vm_already_running())
    else:
        vb_manage_command(
            ['startvm', emulator_name],
            ctx.obj.get_type_output(verbose),
            ['.+error.+']
        )


@click.group(name='screenshot', invoke_without_command=True)
@click.pass_context
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def emulator_screenshot(ctx: {}, verbose: bool):
    """Take screenshot emulator."""

    emulator_name = vm_search_emulator_aurora(VerboseType.none)

    if vm_check_is_run(emulator_name):
        # Screenshot path directory
        screenshot_dir = Path.home() / 'Pictures' / 'Screenshots'

        # Create is not exist
        if screenshot_dir.is_dir():
            screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Screenshot name
        screenshot_name = gen_file_name('Screenshot_from_', 'png')

        # Screenshot path
        screenshot_path = screenshot_dir / screenshot_name

        # Check verbose
        verbose = ctx.obj.get_type_output(verbose)

        # Run command for take screenshot
        result = vb_manage_command(
            ['controlvm', emulator_name, 'screenshotpng', str(screenshot_path)],
            VerboseType.none if verbose == VerboseType.short else verbose,
        )

        # Output
        if verbose == VerboseType.short or verbose == VerboseType.verbose:
            if result:
                echo_stdout(AppTexts.emulator_screenshot_error())
            else:
                echo_stdout(AppTexts.emulator_screenshot_success(str(screenshot_path)))

    else:
        echo_stdout(AppTexts.vm_is_not_running())


@click.group(name='recording', invoke_without_command=True)
@click.pass_context
@click.option('-c', '--convert', is_flag=True, help='Convert video to mp4')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def emulator_recording(ctx: {}, convert: bool, verbose: bool):
    """Recording video from emulator."""

    # Required ffmpeg dependency for convert
    if convert:
        check_dependency_ffmpeg()

    emulator_name = vm_search_emulator_aurora(VerboseType.none)

    # Check verbose
    verbose = ctx.obj.get_type_output(verbose)

    if vm_check_is_run(emulator_name):
        # Video path directory
        video_dir = Path.home() / 'Videos'

        # Create is not exist
        if video_dir.is_dir():
            video_dir.mkdir(parents=True, exist_ok=True)

        # Video name
        video_name = gen_file_name('Video_from_', 'webm')

        # Video path
        video_path = video_dir / video_name

        # Run command for take screenshot
        result = vb_manage_command(
            ['controlvm', emulator_name, 'recording', 'on'],
            VerboseType.none if verbose == VerboseType.short else verbose,
        )

        # Output not empty - error
        if result:
            echo_stdout(AppTexts.emulator_video_record_start_error())
            exit(1)

        # Output start success
        echo_stdout(AppTexts.emulator_video_record_start())

        # Loading record
        click.prompt(
            text=AppTexts.emulator_video_record_prompt(),
            prompt_suffix='',
            default='Enter',
            hide_input=True
        )

        # Run command for take screenshot
        vb_manage_command(
            ['controlvm', emulator_name, 'recording', 'off'],
            VerboseType.none if verbose == VerboseType.short else verbose,
        )

        default_path = Path(
            get_path_file(
                '~/AuroraOS/emulator/{name}/{name}/{name}-screen0.webm'.format(name=emulator_name)
            )
        )

        if not default_path.is_file():
            echo_stderr(AppTexts.file_not_found(str(default_path)))
            exit(1)

        if convert:
            video_path = str(video_path).replace('webm', 'mp4')
            output = None if verbose == VerboseType.verbose else subprocess.DEVNULL
            # Move file with convert
            subprocess.run([
                'ffmpeg',
                '-i',
                str(default_path),
                '-c:v',
                'libx264',
                '-preset',
                'slow',
                '-crf',
                '22',
                '-c:a',
                'aac',
                '-b:a',
                '128k',
                str(video_path),
            ], stdout=output, stderr=output)
        else:
            # Move file
            shutil.move(default_path, video_path)

        # Output stop success
        echo_stdout(AppTexts.emulator_video_record_success(str(video_path)))
    else:
        echo_stdout(AppTexts.vm_is_not_running())
