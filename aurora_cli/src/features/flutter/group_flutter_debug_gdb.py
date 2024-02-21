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

import click

from aurora_cli.src.features.devices.impl.utils import device_ssh_select
from aurora_cli.src.features.flutter.impl.utils import get_spec_keys, GDB_INIT_DATA, GDB_VSCODE_DATA
from aurora_cli.src.support.conf import Conf
from aurora_cli.src.support.dependency import check_dependency_vscode_plugin
from aurora_cli.src.support.dependency_required import check_dependency_vscode, check_dependency_gdb_multiarch
from aurora_cli.src.support.helper import pc_command, find_path_file
from aurora_cli.src.support.output import VerboseType, echo_stdout, echo_stderr
from aurora_cli.src.support.ssh import download_file_sftp, ssh_client_exec_command
from aurora_cli.src.support.texts import AppTexts


@click.group(name='gdb', invoke_without_command=True)
@click.pass_context
@click.option('-i', '--index', type=click.INT, help='Specify index device')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def group_flutter_debug_gdb(ctx: {}, index: int, verbose: bool):
    """Project configure and run on device for gdb debug."""

    port_gdb_server = 2345

    echo_stdout(AppTexts.preparing())

    # Get device client
    client, data = device_ssh_select(ctx, index)

    # Required dependency
    check_dependency_vscode()
    check_dependency_gdb_multiarch()

    # Install vscode extensions
    for extension in [
        'webfreak.debug',
        'ms-vscode.cpptools-extension-pack'
    ]:
        if not check_dependency_vscode_plugin(extension):
            echo_stdout(AppTexts.debug_install_vs_extension(extension))
            pc_command(['code', '--install-extension', extension], VerboseType.none)

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
    if not package_name or not version or not release:
        echo_stderr(AppTexts.flutter_project_read_spec_error())
        exit(1)

    file_path = download_file_sftp(client,
                                   download_path='/usr/bin/{}'.format(package_name),
                                   file_path=Conf.get_temp_folder())

    if not file_path:
        echo_stderr(AppTexts.debug_error_launch_bin())
        exit(1)

    # Get path to launch.json
    vscode_dir = Path(f'{os.getcwd()}/.vscode')
    vscode_dir.mkdir(parents=True, exist_ok=True)
    launch = Path(f'{vscode_dir}/launch.json')

    if launch.is_file():
        if not click.confirm(AppTexts.debug_configure_confirm('launch.json')):
            exit(0)

    # Get path to .gdbinit
    gdbinit = Path(f'{os.getcwd()}/.gdbinit')
    gdbinit.unlink(missing_ok=True)

    # Create .gdbinit app flutter
    with open(gdbinit, 'w') as file:
        print(GDB_INIT_DATA.format(package=package_name), file=file)

    # Create launch.json app flutter
    launch.unlink(missing_ok=True)
    with open(launch, 'w') as file:
        print(GDB_VSCODE_DATA.format(
            rmp_path=file_path,
            ip=data['ip'],
            port=port_gdb_server,
        ), file=file)

    # Run server
    ssh_client_exec_command(
        client,
        'gdbserver --multi :{}'.format(port_gdb_server),
        ctx.obj.get_type_output(verbose)
    )
