import os

from paramiko.client import SSHClient

from aurora_cli.src.support.helper import get_path_files
from aurora_cli.src.support.output import VerboseType, echo_stderr, echo_line, echo_stdout
from aurora_cli.src.support.ssh import ssh_client_exec_command, upload_file_sftp
from aurora_cli.src.support.texts import AppTexts


# Execute the command on the device
def common_command(
        client: SSHClient,
        execute: str,
        verbose: VerboseType
):
    # Execute command
    ssh_client_exec_command(client, execute, verbose, ['^bash.+'])

    # Close ssh client
    client.close()


# Run package on device in container
def common_run(
        client: SSHClient,
        package: str,
        verbose: VerboseType
):
    # Exec command
    execute = 'invoker --type=qt5 {package}'.format(package=package)

    # Execute command
    ssh_client_exec_command(client, execute, verbose, ['.+died.+'])

    # Close ssh client
    client.close()


# Install RPM package on device
def common_install(
        client: SSHClient,
        path: [],
        data: {},
        verbose: VerboseType
):
    # Read paths
    paths = get_path_files(path, extension='rpm')

    if not paths:
        echo_stderr(AppTexts.file_no_one_not_found())
        exit(1)

    # Folder upload
    upload_path = '/home/defaultuser/Downloads'

    for path in paths:
        echo_line()
        echo_stdout(AppTexts.start_upload(path))
        if upload_file_sftp(client, upload_path, path):
            # Get file name
            file_name = os.path.basename(path)
            # Exec command
            if data:
                execute = 'echo {} | {} {upload_path}/{file_name}'.format(
                    data['devel-su'],
                    'devel-su pkcon -y install-local',
                    upload_path=upload_path,
                    file_name=file_name
                )
            else:
                execute = '{} {upload_path}/{file_name}'.format(
                    'pkcon -y install-local',
                    upload_path=upload_path,
                    file_name=file_name
                )
            echo_line()
            if verbose != VerboseType.verbose:
                echo_stdout(AppTexts.package_install_loading())
            # Execute command
            ssh_client_exec_command(client, execute, verbose, ['^error.+', '.+error.+'])

    # Close ssh client
    client.close()


# Upload file to ~/Download directory device
def common_upload(
        client: SSHClient,
        path: [],
):
    # Read paths
    paths = get_path_files(path)

    if not paths:
        echo_stderr(AppTexts.file_no_one_not_found())
        exit(1)

    # Folder upload
    upload_path = '/home/defaultuser/Downloads'

    for path in paths:
        echo_line()
        echo_stdout(AppTexts.start_upload(path))
        upload_file_sftp(client, upload_path, path)

    # Close ssh client
    client.close()
