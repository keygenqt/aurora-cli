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

from aurora_cli.src.base.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.common.texts.info import TextInfo
from aurora_cli.src.base.common.texts.prompt import TextPrompt
from aurora_cli.src.base.common.texts.success import TextSuccess
from aurora_cli.src.base.output import echo_stdout, OutResult
from aurora_cli.src.common.emulator.ssh_features import (
    ssh_command,
    get_ssh_client_emulator,
    ssh_run,
    ssh_upload,
    ssh_rpm_install,
    ssh_rpm_remove
)
from aurora_cli.src.common.emulator.vm_features import (
    vm_emulator_start,
    vm_emulator_screenshot,
    vm_emulator_record_start,
    vm_emulator_record_stop,
)


@click.group(name='emulator')
def group_emulator():
    """Working with the emulator virtualbox."""
    pass


@group_emulator.command(name='start')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def vm_emulator_start_cli(verbose: bool):
    """Start emulator."""
    echo_stdout(vm_emulator_start(), verbose)


@group_emulator.command(name='screenshot')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def vm_emulator_screenshot_cli(verbose: bool):
    """Emulator take screenshot."""
    echo_stdout(vm_emulator_screenshot(), verbose)


@group_emulator.command(name='recording')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def vm_emulator_record_cli(verbose: bool):
    """Recording video from emulator."""
    # Start record
    result = vm_emulator_record_start()
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
    echo_stdout(vm_emulator_record_stop(), verbose)


@group_emulator.command(name='command')
@click.option('-e', '--execute', type=click.STRING, required=True, help='The command to be executed on the emulator')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_command_cli(execute: str, verbose: bool):
    """Execute the command on the emulator."""
    # Get path to key
    result = get_ssh_client_emulator()
    if result.is_error():
        echo_stdout(result)
        exit(1)
    # Run base command
    result = ssh_command(
        client=result.value,
        execute=execute
    )
    if result.is_error():
        echo_stdout(result, verbose)
    else:
        echo_stdout(OutResult(
            message=TextSuccess.ssh_exec_command_success(
                execute=execute,
                stdout='\n'.join(result.value['stdout']),
                stderr='\n'.join(result.value['stderr'])
            )
        ), verbose)


@group_emulator.command(name='run')
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_run_cli(package: str, verbose: bool):
    """Run package on emulator in container."""
    result = get_ssh_client_emulator()
    if result.is_error():
        echo_stdout(result)
        exit(1)
    echo_stdout(ssh_run(
        client=result.value,
        package=package,
        listen_stdout=lambda stdout: echo_stdout(stdout),
        listen_stderr=lambda stderr: echo_stdout(stderr),
    ), verbose)


@group_emulator.command(name='upload')
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to file')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_upload_cli(path: [], verbose: bool):
    """Upload file to ~/Download directory emulator."""
    result = get_ssh_client_emulator()
    if result.is_error():
        echo_stdout(result)
        exit(1)
    for file_path in path:
        echo_stdout(OutResult(TextInfo.shh_download_start(file_path)))
        bar = AliveBarPercentage()
        echo_stdout(ssh_upload(
            client=result.value,
            path=file_path,
            listen_progress=lambda stdout: bar.update(stdout.value)
        ))
    if verbose:
        echo_stdout(OutResult(), verbose)


@group_emulator.command(name='rpm-install')
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-a', '--apm', is_flag=True, help='Use new install APM')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_install_cli(path: [], apm: bool, verbose: bool):
    """Install RPM package on emulator."""
    result = get_ssh_client_emulator('root')
    if result.is_error():
        echo_stdout(result)
        exit(1)

    def bar_update(ab: AliveBarPercentage, percent: int):
        ab.update(percent)
        if percent == 100:
            echo_stdout(OutResult(TextInfo.ssh_install_rpm()))

    for file_path in path:
        echo_stdout(OutResult(TextInfo.shh_download_start(file_path)))
        bar = AliveBarPercentage()
        echo_stdout(ssh_rpm_install(
            client=result.value,
            path=file_path,
            apm=apm,
            listen_progress=lambda stdout: bar_update(bar, stdout.value)
        ))
    if verbose:
        echo_stdout(OutResult(), verbose)


@group_emulator.command(name='rpm-remove')
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-a', '--apm', is_flag=True, help='Use new install APM')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_install_cli(package: str, apm: bool, verbose: bool):
    """Install RPM package on emulator."""
    result = get_ssh_client_emulator('root')
    if result.is_error():
        echo_stdout(result)
        exit(1)
    echo_stdout(ssh_rpm_remove(
        client=result.value,
        package=package,
        apm=apm,
    ), verbose)
