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

from aurora_cli.src.base.common.vm_features import vm_emulator_record_stop
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.utils.app import app_crash_out
from aurora_cli.src.base.utils.argv import argv_is_emulator_recording
from aurora_cli.src.base.utils.click import click_init_groups


# If the application was closed via ctrl+c, you need to end running tasks
# But the application context is closed along with it
# The `abort` group recreates it by repeating the `main` group
# Once the context is restored, running tasks can be completed
# A good example of such a task is running a recording in the emulator
def clear_after_force_close():
    try:
        try:
            click_init_groups(abort)
            abort(standalone_mode=False)
        except click.exceptions.Abort:
            clear_after_force_close()
    except Exception as e:
        app_crash_out(e)


@click.group(invoke_without_command=True)
@click.option('--config', help='Specify config path.', type=click.STRING, required=False)
@click.pass_context
def abort(ctx: {}, config: str):
    ctx.obj = AppConfig.create(config)
    print('Aborted! Closing...')

    # Stop recording video if recording
    if argv_is_emulator_recording():
        vm_emulator_record_cli()

    print('Goodbye 👋')
    exit(1)


def vm_emulator_record_cli():
    """Stop recording video from emulator."""
    vm_emulator_record_stop()
