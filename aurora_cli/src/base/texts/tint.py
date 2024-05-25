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
import subprocess

from aurora_cli.src.base.constants.other import VM_MANAGE


def tint(func):
    def wrapped(*args, **kwargs) -> str:
        match func.__name__:
            case 'emulator_not_found_running':
                return tint_emulator_run(func(*args, **kwargs))
            case 'dependency_not_found':
                return tint_install_app(func(*args, **kwargs), *args)
            case 'validate_config_devices_not_found' \
                 | 'validate_config_devices' \
                 | 'validate_config_keys_not_found' \
                 | 'validate_config_keys' \
                 | 'validate_config_workdir_not_found' \
                 | 'config_arg_path_load_error':
                return tint_config_help(func(*args, **kwargs))

    return wrapped


def tint_emulator_run(text: str):
    return '{text}\n{tint}'.format(
        text=text,
        tint='<i>You can start the emulator with the following command:</i> aurora-cli emulator start'
    )


def tint_config_help(text: str):
    return '{text}\n{tint}'.format(
        text=text,
        tint='<i>Check the application documentation:</i> https://keygenqt.github.io/aurora-cli'
    )


def tint_install_app(text: str, *args):
    try:
        subprocess.run(['apt', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        application = args[0]
        if application == VM_MANAGE:
            application = 'virtualbox'

        return '{text}\n{tint}'.format(
            text=text,
            tint=f'<i>You need to install this application:</i> sudo apt install {application}'
        )
    except (Exception,):
        return '{text}\n{tint}'.format(
            text=text,
            tint='<i>You need to install this application.</i>'
        )
