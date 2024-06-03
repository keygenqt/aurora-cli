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
from typing import Callable

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
        nohup: bool,
        listen_stdout: Callable[[OutResult | None], None],
        listen_stderr: Callable[[OutResult | None], None],
        close: bool = True
) -> OutResult:
    def check_is_error(out: str) -> bool:
        if 'could not locate' in out:
            return True
        if 'invoker: error' in out:
            return True
        return False

    if nohup:
        execute = f'nohup invoker --type=qt5 {package}'
    else:
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
    return OutResult()


def ssh_upload(
        client: SSHClient,
        path: str,
        listen_progress: Callable[[OutResult], None],
        close: bool = True
) -> OutResult:
    cache_progress = []

    def call_calculate_progress(transferred: int, total: int):
        progress = int(transferred * 100 / total) if total != 0 else 0
        if progress not in cache_progress:
            cache_progress.append(progress)
            listen_progress(OutResultInfo(
                message=TextInfo.shh_upload_progress(),
                value=progress
            ))

    file_path = path_convert_relative(path)

    if not file_path.is_file():
        return OutResultError(
            message=TextError.ssh_upload_file_not_found(path),
        )

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
        listen_progress: Callable[[OutResult], None],
        devel_su: str | None = None,
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
        prompt = "{'ShowPrompt': <false>}"
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
            value={
                'stdout': stdout,
                'stderr': stderr,
            }
        )

    return OutResult(TextSuccess.ssh_install_rpm(os.path.basename(file_upload)))


def ssh_package_remove(
        client: SSHClient,
        package: str,
        apm: bool,
        devel_su: str | None = None,
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
                   f'"{package}"')

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

    return OutResult(TextSuccess.ssh_remove_rpm())
