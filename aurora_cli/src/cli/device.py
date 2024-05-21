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

from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.output import echo_stdout, OutResult
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.common.ssh_features import ssh_command


@click.group(name='device')
def group_device():
    """Working with the device."""
    pass


@group_device.command(name='command')
@click.option('-e', '--execute', type=click.STRING, required=True, help='The command to be executed on the device')
@click.option('-s', '--select', is_flag=True, help='Select from available')
@click.option('-i', '--index', type=click.INT, default=None, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_command_cli(execute: str, select: bool, index: int | None, verbose: bool):
    """Execute the command on the device."""
    if select and index is None:
        echo_stdout(TextInfo.select_array_out(
            key='devices',
            names=DeviceModel.get_names_devices(),
        ))
    result = DeviceModel.get_model_select(select, index)
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    result = result.value.get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
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


@group_device.command(name='run')
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-s', '--select', is_flag=False, help='Select from available')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_run_cli(package: str, select: bool, index: int, verbose: bool):
    """Run package on device in container."""
    pass
    # result = EmulatorModel.get_model_user().get_ssh_client()
    # if result.is_error():
    #     echo_stdout(result)
    #     exit(1)
    # echo_stdout(ssh_run(
    #     client=result.value,
    #     package=package,
    #     listen_stdout=lambda stdout: echo_stdout(stdout),
    #     listen_stderr=lambda stderr: echo_stdout(stderr),
    # ), verbose)


@group_device.command(name='upload')
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to file')
@click.option('-s', '--select', is_flag=False, help='Select from available')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_upload_cli(path: [], select: bool, index: int, verbose: bool):
    """Upload file to ~/Download directory device."""
    pass
    # result = EmulatorModel.get_model_user().get_ssh_client()
    # if result.is_error():
    #     echo_stdout(result)
    #     exit(1)
    # for file_path in path:
    #     echo_stdout(OutResult(TextInfo.shh_download_start(file_path)))
    #     bar = AliveBarPercentage()
    #     echo_stdout(ssh_upload(
    #         client=result.value,
    #         path=file_path,
    #         listen_progress=lambda stdout: bar.update(stdout.value)
    #     ))
    # if verbose:
    #     echo_stdout(OutResult(), verbose)


@group_device.command(name='package-install')
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-a', '--apm', is_flag=True, help='Use new install APM')
@click.option('-s', '--select', is_flag=False, help='Select from available')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_install_cli(path: [], apm: bool, select: bool, index: int, verbose: bool):
    """Install RPM package on device."""
    pass
    # result = EmulatorModel.get_model_root().get_ssh_client()
    # if result.is_error():
    #     echo_stdout(result)
    #     exit(1)
    #
    # def bar_update(ab: AliveBarPercentage, percent: int):
    #     ab.update(percent)
    #     if percent == 100:
    #         echo_stdout(OutResult(TextInfo.ssh_install_rpm()))
    #
    # for file_path in path:
    #     echo_stdout(OutResult(TextInfo.shh_download_start(file_path)))
    #     bar = AliveBarPercentage()
    #     echo_stdout(ssh_rpm_install(
    #         client=result.value,
    #         path=file_path,
    #         apm=apm,
    #         listen_progress=lambda stdout: bar_update(bar, stdout.value)
    #     ))
    # if verbose:
    #     echo_stdout(OutResult(), verbose)


@group_device.command(name='package-remove')
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-a', '--apm', is_flag=True, help='Use new install APM')
@click.option('-s', '--select', is_flag=False, help='Select from available')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_remove_cli(package: str, apm: bool, select: bool, index: int, verbose: bool):
    """Install RPM package on device."""
    pass
    # result = get_ssh_client_emulator('root')
    # if result.is_error():
    #     echo_stdout(result)
    #     exit(1)
    # echo_stdout(ssh_rpm_remove(
    #     client=result.value,
    #     package=package,
    #     apm=apm,
    # ), verbose)
