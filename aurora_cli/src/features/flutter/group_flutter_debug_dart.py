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
import os
from pathlib import Path
from threading import Timer

import click

from aurora_cli.src.features.devices.impl.utils import device_ssh_select, emulator_ssh_select
from aurora_cli.src.features.flutter.impl.utils import get_spec_keys, DART_VSCODE_DATA, \
    CUSTOM_DEVICE_CODE_DATA, get_list_flutter_installed, CUSTOM_DEVICE_CODE_DATA_VM
from aurora_cli.src.support.dependency import check_dependency_vscode_plugin, check_dependency_sshpass
from aurora_cli.src.support.dependency_required import check_dependency_vscode
from aurora_cli.src.support.helper import pc_command, find_path_file, prompt_index
from aurora_cli.src.support.output import VerboseType, echo_stdout, echo_stderr
from aurora_cli.src.support.sdk import find_folder_sdk
from aurora_cli.src.support.ssh import ssh_client_exec_command
from aurora_cli.src.support.texts import AppTexts


@click.group(name='dart', invoke_without_command=True)
@click.pass_context
@click.option('-i', '--index', type=click.INT, help='Specify index device')
@click.option('-e', '--emulator', is_flag=True, default=False, help="Run on emulator")
@click.option('-y', '--yes', is_flag=True, help='All yes confirm')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def group_flutter_debug_dart(ctx: {}, index: int, emulator: bool, yes: bool, verbose: bool):
    """Project configure and run on device for dart debug or hot reload."""

    workdir = ctx.obj.get_workdir()
    sdk_path = find_folder_sdk(workdir)

    # Required dependency
    check_dependency_vscode()

    # Required flutter
    versions = get_list_flutter_installed()
    if not versions:
        echo_stderr(AppTexts.flutter_not_found())
        exit(0)

    # Get path application
    application = Path(f'{os.getcwd()}/example')
    if not application.is_dir():
        application = Path(os.getcwd())

    # Find spec app flutter
    file_spec = find_path_file('spec', Path(f'{application}/aurora/rpm'))
    if not file_spec or not file_spec.is_file():
        echo_stderr(AppTexts.debug_is_not_flutter_aurora_project())
        exit(1)

    # Get package keys
    package_name, version, release = get_spec_keys(file_spec)

    # Required project folder
    if not package_name or not version or not release:
        echo_stderr(AppTexts.flutter_project_read_spec_error())
        exit(1)

    # Select flutter
    echo_stdout(AppTexts.select_versions(versions))
    echo_stdout(AppTexts.array_indexes(versions), 2)
    flutter = Path.home() / '.local' / 'opt' / 'flutter-{}'.format(versions[prompt_index(versions)]) / 'bin' / 'flutter'

    # Install vscode extensions
    for extension in [
        'dart-code.dart-code',
        'dart-code.flutter'
    ]:
        if not check_dependency_vscode_plugin(extension):
            echo_stdout(AppTexts.debug_install_vs_extension(extension))
            pc_command(['code', '--install-extension', extension], VerboseType.none)

    # Enable custom device in flutter
    pc_command([
        flutter,
        'config',
        '--enable-custom-devices',
    ], VerboseType.none)

    if emulator:
        client = emulator_ssh_select(workdir=workdir)
        device_ip = '127.0.0.1'
    else:
        client, data = device_ssh_select(ctx, index)
        device_ip = data['ip']
        device_pass = data['pass']

    # Get path to launch.json
    vscode_dir = Path(f'{os.getcwd()}/.vscode')
    vscode_dir.mkdir(parents=True, exist_ok=True)
    launch = Path(f'{vscode_dir}/launch.json')

    # Confirm rewrite file
    if launch.is_file() and not yes:
        if not click.confirm(AppTexts.debug_configure_confirm('launch.json')):
            exit(0)

    # Get path to custom_devices.json
    config_dir = Path(f'{Path.home()}/.config/flutter')
    config_dir.mkdir(parents=True, exist_ok=True)
    custom_devices = Path(f'{config_dir}/custom_devices.json')

    # Confirm rewrite file
    if custom_devices.is_file() and not yes:
        if not click.confirm(AppTexts.debug_configure_confirm('custom_devices.json')):
            exit(0)

    def rewrite_configs(url: str, ip: str):
        # Create custom_devices.json
        custom_devices.unlink(missing_ok=True)
        with open(custom_devices, 'w') as file:
            if emulator:
                print(CUSTOM_DEVICE_CODE_DATA_VM.format(
                    ip=ip,
                    package=package_name,
                    sdk_path=sdk_path
                ), file=file)
            else:
                print(CUSTOM_DEVICE_CODE_DATA.format(
                    ip=ip,
                    package=package_name,
                ), file=file)
        # Create launch.json
        launch.unlink(missing_ok=True)
        with open(launch, 'w') as f:
            print(DART_VSCODE_DATA.format(
                vm_service_uri=url,
                main_path=('example/lib/main.dart' if 'example' in str(application) and str(
                    application) != os.getcwd() else 'lib/main.dart')
            ), file=f)

    def device_check_and_set_ssh_key():
        ssh_key = Path.home() / '.ssh' / 'id_rsa'
        if not ssh_key.is_file():
            echo_stderr(AppTexts.error_find_ssh_key(str(ssh_key)))
            exit(1)
        if not check_dependency_sshpass():
            echo_stderr(AppTexts.error_dependency_sshpass())
            exit(1)
        pc_command([
            'sshpass',
            '-p{}'.format(device_pass),
            'ssh-copy-id',
            '-i',
            str(ssh_key),
            'defaultuser@{ip}'.format(ip=device_ip),
        ], VerboseType.none)

    def ssh_nfl(port: int):
        if emulator:
            pc_command([
                'ssh',
                '-i',
                '{sdk_path}/vmshare/ssh/private_keys/sdk'.format(sdk_path=sdk_path),
                '-NfL',
                '{port}:127.0.0.1:{port}'.format(port=port),
                'defaultuser@{ip}'.format(ip=device_ip),
                '-p2223'
            ], VerboseType.verbose)
        else:
            pc_command([
                'ssh',
                '-NfL',
                '{port}:127.0.0.1:{port}'.format(port=port),
                'defaultuser@{ip}'.format(ip=device_ip),
            ], VerboseType.verbose)

    # If device check ssh key
    if not emulator:
        device_check_and_set_ssh_key()

    # Loading 10 second link from app
    def exit_not_debug_run():
        echo_stderr(AppTexts.debug_error_launch_debug_app())
        exit(1)
        os._exit(1)

    # Run timer
    debug_check_run = Timer(10.0, exit_not_debug_run)
    debug_check_run.start()

    def update_launch(line: str, _: int):
        if '-bash' in line:
            echo_stderr(AppTexts.debug_error_launch_bin())
            exit(1)
        if 'listening on ' in line:
            url = line.split('listening on ')[1]
            rewrite_configs(url, device_ip)
            ssh_nfl(int(url.split('/')[2].split(':')[1]))
            debug_check_run.cancel()

    # Exec command
    execute = '/usr/bin/{}'.format(package_name)

    # Execute command
    ssh_client_exec_command(
        client,
        execute,
        ctx.obj.get_type_output(verbose),
        None,
        callback=update_launch
    )

    # Close ssh client
    client.close()
