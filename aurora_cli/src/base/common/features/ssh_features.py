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
from typing import Callable, Any

import rpmfile
from paramiko.client import SSHClient

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import OutResult, OutResultError, OutResultInfo
from aurora_cli.src.base.utils.path import path_convert_relative
from aurora_cli.src.base.utils.ssh import ssh_exec_command


def ssh_command(
        client: SSHClient,
        execute: str,
        close: bool = True
) -> OutResult:
    stdout, stderr = ssh_exec_command(client, execute)
    if close:
        client.close()
    return OutResult(
        message=TextSuccess.ssh_exec_command_success(
            execute=execute
        ),
        value={
            'stdout': stdout,
            'stderr': stderr,
        }
    )


def ssh_run(
        client: SSHClient,
        package: str,
        run_mode: Any,  # dart/gdb/sandbox
        listen_stdout: Callable[[Any], None],
        listen_stderr: Callable[[Any], None],
        close: bool = True
) -> OutResult:
    def check_is_error(out: str) -> bool:
        if 'could not locate' in out:
            return True
        if 'invoker: error' in out:
            return True
        return False

    if run_mode == 'dart':
        execute = f'env LD_LIBRARY_PATH=/opt/app/{package}/current/data/lib /usr/bin/{package}'
    elif run_mode == 'gdb':
        execute = f'gdbserver --multi :2345'
    else:
        # sandbox
        execute = f'invoker --type=qt5 {package}'

    stdout, stderr = ssh_exec_command(
        client=client,
        execute=execute,
        listen_stdout=lambda value, index: listen_stdout(
            None if check_is_error(value) else OutResult(value=value, index=index)
        ),
        listen_stderr=lambda value, index: listen_stderr(
            None if check_is_error(value) else OutResult(value=value, index=index)
        ),
    )

    if close:
        client.close()

    if stderr or (stdout and check_is_error(stdout[0])):
        return OutResultError(
            message=TextError.ssh_run_application_error(package),
            value=stdout + stderr
        )
    return OutResult(TextSuccess.ssh_run_package(package))


def ssh_download(
        client: SSHClient,
        path_remote: str,
        path_local: str,
        force: bool = False,
        close: bool = True
) -> OutResult:
    try:
        path_local = path_convert_relative(path_local)

        if path_local.is_file():
            if force:
                path_local.unlink(missing_ok=True)
            else:
                return OutResultError(TextError.file_already_exists_error(str(path_local)))

        client.open_sftp().get(
            remotepath=path_remote,
            localpath=path_local,
        )
        if close:
            client.close()
        return OutResult(
            message=TextSuccess.ssh_download_success(str(path_local)),
            value={
                'localpath': str(path_local),
                'remotepath': str(path_remote),
            }
        )
    except Exception as e:
        print(e)

        return OutResultError(
            message=TextError.ssh_download_error(),
            value=str(e)
        )


def ssh_upload(
        client: SSHClient,
        path: str,
        listen_progress: Callable[[OutResult], None],
        close: bool = True
) -> OutResult:
    cache_progress = []

    def call_calculate_progress(transferred: int, total: int):
        if listen_progress:
            progress = int(transferred * 100 / total) if total != 0 else 0
            if progress not in cache_progress:
                cache_progress.append(progress)
                listen_progress(OutResultInfo(
                    message=TextInfo.shh_upload_progress(),
                    value=progress
                ))

    file_path = path_convert_relative(path)

    if not file_path.is_file():
        return OutResultError(TextError.file_not_found_error(path))

    try:
        file_name = os.path.basename(file_path)
        file_upload = f'/home/defaultuser/Downloads/{file_name}'
        call_calculate_progress(0, 0)
        client.open_sftp().put(
            localpath=file_path,
            remotepath=file_upload,
            callback=lambda transferred, total: call_calculate_progress(transferred, total)
        )
        if close:
            client.close()
        return OutResult(
            message=TextSuccess.ssh_uploaded_success(file_upload),
            value={
                'localpath': str(file_path),
                'remotepath': str(file_upload),
            }
        )
    except Exception as e:
        return OutResultError(
            message=TextError.ssh_upload_error(),
            value=str(e)
        )


def ssh_rpm_install(
        client: SSHClient,
        path: str,
        apm: bool,
        reinstall: bool,
        listen_progress: Callable[[OutResult], None],
        devel_su: Any = None,
        close: bool = True
) -> OutResult:
    def check_is_error(out: []) -> bool:
        for line in out:
            if 'Error:' in line:
                return True
            if 'Fatal error' in line:
                return True
        return False

    result = ssh_upload(client, path, listen_progress, close=False)
    if result.is_error():
        return result

    file_upload = result.value['remotepath']

    if not apm:
        if devel_su:
            execute = f'echo {devel_su} | devel-su pkcon -y install-local {file_upload}'
        else:
            execute = f'pkcon -y install-local {file_upload}'
    else:
        if reinstall:
            package_installed = False

            with rpmfile.open(path) as rpm:
                if package_as_bytes := rpm.headers.get('name'):
                    package = package_as_bytes.decode("utf-8")
                    package_installed = ssh_check_package_installed(client, package, close=False)

            if package_installed:
                for use_apm in [False, True]:
                    package_removed = ssh_package_remove(
                        client,
                        package,
                        apm=use_apm,
                        keep_user_data=True,
                        devel_su=devel_su,
                        close=False,
                    ).is_success()

                    if package_removed:
                        break

                if not package_removed:
                    return OutResultError(TextError.ssh_remove_rpm_error())

        prompt = "{}"
        execute = (f'gdbus call --system '
                   f'--dest ru.omp.APM '
                   f'--object-path /ru/omp/APM '
                   f'--method ru.omp.APM.Install '
                   f'"{file_upload}" '
                   f'"{prompt}"')

    stdout, stderr = ssh_exec_command(client, execute)
    if close:
        client.close()

    if check_is_error(stdout) or stderr:
        return OutResultError(
            message=TextError.ssh_install_rpm_error(),
            value={'stdout': stdout, 'stderr': stderr}
        )

    return OutResult(TextSuccess.ssh_install_rpm(os.path.basename(file_upload)))


def ssh_package_remove(
        client: SSHClient,
        package: str,
        apm: bool,
        keep_user_data: bool,
        devel_su: Any = None,
        close: bool = True
) -> OutResult:
    def check_is_error(out: []) -> bool:
        for line in out:
            if 'Error:' in line:
                return True
            if 'Package not found' in line:
                return True
        return False

    if not apm:
        if devel_su:
            execute = f'echo {devel_su} | devel-su pkcon -y remove {package}'
        else:
            execute = f'pkcon -y remove {package}'
    else:
        execute = (f'gdbus call --system '
                   f'--dest ru.omp.APM '
                   f'--object-path /ru/omp/APM '
                   f'--method ru.omp.APM.Remove '
                   f'"{package}" ')

    apm_use_legacy_api = True
    stdout, stderr = ssh_exec_command(client, execute)

    if stdout and 'Invalid arguments' in stdout[0]:
        apm_use_legacy_api = False
        prompt = "{'KeepUserData': <true>}" if keep_user_data else "{}"
        execute += f'"{prompt}"'
        stdout, stderr = ssh_exec_command(client, execute)

    if close:
        client.close()

    if check_is_error(stdout) or stderr:
        return OutResultError(
            message=TextError.ssh_remove_rpm_error(),
            value={
                'stdout': stdout,
                'stderr': stderr,
            }
        )

    if keep_user_data:
        if not apm:
            return OutResult(TextSuccess.ssh_remove_rpm_without_keeping_hint())
        elif apm_use_legacy_api:
            return OutResult(TextSuccess.ssh_remove_rpm_without_keeping_hint())

    return OutResult(TextSuccess.ssh_remove_rpm())


def ssh_get_device_platform_name(
        client: SSHClient,
        close: bool = True
) -> Any:
    execute = 'cat /etc/os-release'
    stdout, stderr = ssh_exec_command(client, execute)

    if close:
        client.close()

    if stderr:
        return None
    for line in stdout:
        if 'VERSION_ID=' in line:
            return line.split('=')[-1]
    return None


def ssh_get_device_platform_arch(
        client: SSHClient,
        close: bool = True
) -> Any:
    execute = 'cat /etc/rpm/platform'
    stdout, stderr = ssh_exec_command(client, execute)

    if close:
        client.close()

    if stderr:
        return None
    for line in stdout:
        if 'armv7hl' in line:
            return 'aurora-arm'
        if 'aarch64' in line:
            return 'aurora-arm64'
    return 'aurora-arm'


def ssh_check_package_installed(
        client: SSHClient,
        package: str,
        close: bool = True
) -> bool:
    result = ssh_command(
        client=client,
        execute=f'file /usr/bin/{package}',
        close=close,
    )
    return ': symbolic link to' in result.value['stdout'][0]
