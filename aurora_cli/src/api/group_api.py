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

import sys

import click

from aurora_cli.src.api.routes.routes_app import search_route_app
from aurora_cli.src.api.routes.routes_device import search_route_device
from aurora_cli.src.api.routes.routes_emulator import search_route_emulator
from aurora_cli.src.api.routes.routes_flutter import search_route_flutter
from aurora_cli.src.api.routes.routes_psdk import search_route_psdk
from aurora_cli.src.api.routes.routes_sdk import search_route_sdk
from aurora_cli.src.api.routes.routes_settings import search_route_settings
from aurora_cli.src.api.routes.routes_tests import search_route_tests
from aurora_cli.src.api.routes.routes_vscode import search_route_vscode
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, echo_verbose
from aurora_cli.src.base.utils.route import get_arg_bool
from aurora_cli.src.base.utils.text import text_multiline_help

help_routes = f'''
-- /app -----------------------------------------------------

{TextCommand.command_app_info()}
/app/info

{TextArgument.argument_clear_cache()}
/app/clear

{TextCommand.command_app_versions()}
/app/versions

{TextCommand.command_app_auth_check()}
/app/auth/check
  • version - {TextArgument.argument_psdk_version()}
  
{TextCommand.command_app_auth_root()}
/app/auth/root
  • password - {TextArgument.argument_password()}
  
-- /device --------------------------------------------------

{TextCommand.command_device_list()}
/device/list

{TextCommand.command_device_info()}
/device/info
  • host - {TextArgument.argument_host_device()}

{TextCommand.command_device_command()}
/device/command
  • host - {TextArgument.argument_host_device()}
  • execute - {TextArgument.argument_execute_device()}

{TextCommand.command_device_upload()}
/device/upload
  • host - {TextArgument.argument_host_device()}
  • path - {TextArgument.argument_path()}
    
{TextCommand.command_device_package_run()}
/device/package/run
  • host - {TextArgument.argument_host_device()}
  • package - {TextArgument.argument_package_name()}
  • mode [dart, gdb] ({TextArgument.argument_optional()}) - {TextArgument.argument_run_mode()}
  • project ({TextArgument.argument_optional()}) - {TextArgument.argument_path_to_project()}
    
{TextCommand.command_device_package_install()}
/device/package/install
  • host - {TextArgument.argument_host_device()}
  • path - {TextArgument.argument_path()}
  • apm [default = false, true] - {TextArgument.argument_apm()}
    
{TextCommand.command_device_package_remove()}
/device/package/remove
  • host - {TextArgument.argument_host_device()}
  • package - {TextArgument.argument_package_name()}
  • apm [default = false, true] - {TextArgument.argument_apm()}

-- /emulator -------------------------------------------------

{TextCommand.command_emulator_start()}
/emulator/start

{TextCommand.command_emulator_screenshot()}
/emulator/screenshot

{TextCommand.command_emulator_recording_start()}
/emulator/recording/start

{TextCommand.command_emulator_recording_stop()}
/emulator/recording/stop

{TextCommand.command_emulator_info()}
/emulator/info

{TextCommand.command_emulator_command()}
/emulator/command
  • execute - {TextArgument.argument_execute_emulator()}

{TextCommand.command_emulator_upload()}
/emulator/upload
  • path - {TextArgument.argument_path()}
    
{TextCommand.command_emulator_package_run()}
/emulator/package/run
  • package - {TextArgument.argument_package_name()}
  • mode [dart, gdb] ({TextArgument.argument_optional()}) - {TextArgument.argument_run_mode()}
  • project ({TextArgument.argument_optional()}) - {TextArgument.argument_path_to_project()}
    
{TextCommand.command_emulator_package_install()}
/emulator/package/install
  • path - {TextArgument.argument_path()}
  • apm [default = false, true] - {TextArgument.argument_apm()}
    
{TextCommand.command_emulator_package_remove()}
/emulator/package/remove
  • package - {TextArgument.argument_package_name()}
  • apm [default = false, true] - {TextArgument.argument_apm()}

-- /flutter --------------------------------------------------

{TextCommand.command_flutter_available()}
/flutter/available

{TextCommand.command_flutter_installed()}
/flutter/installed

{TextCommand.command_flutter_install()}
/flutter/install
  • version - {TextArgument.argument_flutter_version()}

{TextCommand.command_flutter_remove()}
/flutter/remove
  • version - {TextArgument.argument_flutter_version()}

{TextCommand.command_flutter_custom_devices()}
/flutter/custom-devices
  • version - {TextArgument.argument_flutter_version()}

{TextCommand.command_project_format()}
/flutter/project/format
  • version - {TextArgument.argument_flutter_version()}
  • path - {TextArgument.argument_path_to_project()}

{TextCommand.command_project_build()}
/flutter/project/build
  • version - {TextArgument.argument_flutter_version()}
  • psdk - {TextArgument.argument_psdk_version()}
  • path - {TextArgument.argument_path_to_project()}
  • target - {TextArgument.argument_target_name()}
  • debug [default = false, true] - {TextArgument.argument_debug()}
  • clean [default = false, true] - {TextArgument.argument_clean()}
  • pub_get [default = false, true] - {TextArgument.argument_pub_get()}
  • build_runner [default = false, true] - {TextArgument.argument_build_runner()}
  • install [default = false, true] - {TextArgument.argument_install()}
  • apm [default = false, true] - {TextArgument.argument_apm()}
  • run [default = false, true] - {TextArgument.argument_run()}
  • verbose [default = false, true] - {TextArgument.argument_verbose()}
  • run_mode [dart, gdb] ({TextArgument.argument_optional()}) - {TextArgument.argument_run_mode()}
  • host ({TextArgument.argument_optional()}) - {TextArgument.argument_host_device()}
  • key ({TextArgument.argument_optional()}) - {TextArgument.argument_key_sign_name()}

{TextCommand.command_flutter_project_report()}
/flutter/project/report
  • version - {TextArgument.argument_flutter_version()}
  • path - {TextArgument.argument_path_to_project()}

{TextCommand.command_project_icon()}
/flutter/project/icons
  • image - {TextArgument.argument_path_to_image()}
  • path - {TextArgument.argument_path_to_project()}
  
-- /psdk -----------------------------------------------------

{TextCommand.command_psdk_available()}
/psdk/available

{TextCommand.command_psdk_installed()}
/psdk/installed

{TextCommand.command_psdk_info()}
/psdk/info
  • version - {TextArgument.argument_psdk_version()}

{TextCommand.command_psdk_targets()}
/psdk/targets
  • version - {TextArgument.argument_psdk_version()}

{TextCommand.command_psdk_download()}
/psdk/download
  • version - {TextArgument.argument_psdk_version()}

{TextCommand.command_psdk_install()}
/psdk/install
  • version - {TextArgument.argument_psdk_version()}

{TextCommand.command_psdk_remove()}
/psdk/remove
  • version - {TextArgument.argument_psdk_version()}

{TextCommand.command_psdk_clear()}
/psdk/clear
  • version - {TextArgument.argument_psdk_version()}
  • target - {TextArgument.argument_target_name()}

{TextCommand.command_psdk_sudoers_add()}
/psdk/sudoers/add
  • version - {TextArgument.argument_psdk_version()}

{TextCommand.command_psdk_sudoers_remove()}
/psdk/sudoers/remove
  • version - {TextArgument.argument_psdk_version()}

{TextCommand.command_psdk_package_search()}
/psdk/package/search
  • version - {TextArgument.argument_psdk_version()}
  • target - {TextArgument.argument_target_name()}
  • package - {TextArgument.argument_package_name()}

{TextCommand.command_psdk_package_install()}
/psdk/package/install
  • version - {TextArgument.argument_psdk_version()}
  • target - {TextArgument.argument_target_name()}
  • path - {TextArgument.argument_path_rpm()}

{TextCommand.command_psdk_package_remove()}
/psdk/package/remove
  • version - {TextArgument.argument_psdk_version()}
  • target - {TextArgument.argument_target_name()}
  • package - {TextArgument.argument_package_name()}

{TextCommand.command_psdk_validate()}
/psdk/package/validate
  • version - {TextArgument.argument_psdk_version()}
  • target - {TextArgument.argument_target_name()}
  • path - {TextArgument.argument_path_rpm()}
  • profile [regular, extended, mdm, antivirus, auth] - {TextArgument.argument_validate_profile()}

{TextCommand.command_psdk_sign()}
/psdk/package/sign
  • version - {TextArgument.argument_psdk_version()}
  • path - {TextArgument.argument_path_rpm()}
  • key ({TextArgument.argument_optional()}) - {TextArgument.argument_key_sign_name()}

{TextCommand.command_project_format()}
/psdk/project/format
  • path - {TextArgument.argument_path_to_project()}

{TextCommand.command_project_build()}
/psdk/project/build
  • version - {TextArgument.argument_psdk_version()}
  • target - {TextArgument.argument_target_name()}
  • path - {TextArgument.argument_path_to_project()}
  • clean [default = false, true] - {TextArgument.argument_clean()}
  • install [default = false, true] - {TextArgument.argument_install()}
  • apm [default = false, true] - {TextArgument.argument_apm()}
  • run [default = false, true] - {TextArgument.argument_run()}
  • debug [default = false, true] - {TextArgument.argument_debug()}
  • verbose [default = false, true] - {TextArgument.argument_verbose()}
  • host ({TextArgument.argument_optional()}) - {TextArgument.argument_host_device()}
  • key ({TextArgument.argument_optional()}) - {TextArgument.argument_key_sign_name()}

{TextCommand.command_project_icon()}
/psdk/project/icons
  • image - {TextArgument.argument_path_to_image()}
  • path - {TextArgument.argument_path_to_project()}

-- /sdk ------------------------------------------------------

{TextCommand.command_sdk_available()}
/sdk/available
  
{TextCommand.command_sdk_installed()}
/sdk/installed
  
{TextCommand.command_sdk_install()}
/sdk/install
  • version - {TextArgument.argument_psdk_version()}
  • offline [default = false, true] - {TextArgument.argument_sdk_installer_type()}
  
{TextCommand.command_sdk_tool()}
/sdk/tool

-- /vscode ---------------------------------------------------

{TextCommand.command_vscode_info()}
/vscode/info

{TextCommand.command_vscode_extensions_list()}
/vscode/extensions/list

{TextCommand.command_vscode_extension_install()}
/vscode/extensions/install
  • extension - {TextArgument.argument_vscode_extension()}

{TextCommand.command_vscode_settings_update()}
/vscode/settings/update

-- /settings -------------------------------------------------

{TextCommand.command_settings_list()}
/settings/list

{TextCommand.command_settings_clear()}
/settings/clear

{TextCommand.command_settings_localization()}
/settings/localization
  • language [ru, en] - {TextArgument.argument_language()}

{TextCommand.command_settings_verbose()}
/settings/verbose
  • enable [false, true] - {TextArgument.argument_enable_verbose()}

{TextCommand.command_settings_select()}
/settings/select
  • enable [false, true] - {TextArgument.argument_enable_save_select()}
  
{TextCommand.command_settings_hint()}
/settings/hint
  • enable [false, true] - {TextArgument.argument_enable_hint()}

-- /tests ----------------------------------------------------

{TextCommand.command_test_answer()}
/tests/answer
  • time [default = 0] - {TextArgument.argument_test_answer_time()}
  • code [default = 200] - {TextArgument.argument_test_answer_code()}
  • iterate [default = 1] - {TextArgument.argument_test_answer_iterate()}
'''


@click.group(name='api', invoke_without_command=True, help=TextGroup.group_api())
@click.option('--route', help=text_multiline_help(help_routes), type=click.STRING, required=True)
def group_api(route: str):
    if argv_is_test():
        sys.argv.append('api')
        AppConfig.create_test()
    try:
        for func in [
            search_route_app,
            search_route_device,
            search_route_emulator,
            search_route_flutter,
            search_route_psdk,
            search_route_sdk,
            search_route_vscode,
            search_route_settings,
            search_route_tests,
        ]:
            if func(route):
                echo_verbose(get_arg_bool(route, 'verbose'))
                exit(0)

        echo_stdout(OutResultError(TextError.route_not_found()))
    except Exception as e:
        echo_stdout(OutResultError(str(e)))
