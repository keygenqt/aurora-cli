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
from typing import Callable

from aurora_cli.src.support.helper import pc_command, check_string_regex
from aurora_cli.src.support.output import VerboseType, echo_stderr
from aurora_cli.src.support.texts import AppTexts

VM_MANAGE = "VBoxManage"


# Search engine name in vb
def vm_search_engine_aurora(verbose: VerboseType) -> str:
    vm = _vm_search_by_regx(['.+Aurora.+Engine.+'], verbose)
    if not vm:
        echo_stderr(AppTexts.vm_not_found())
        exit(1)
    return vm


# Search emulator name in vb
def vm_search_emulator_aurora(verbose: VerboseType) -> str:
    vm = _vm_search_by_regx(['.+AuroraOS.+'], verbose)
    if not vm:
        echo_stderr(AppTexts.vm_not_found())
        exit(1)
    return vm


# Search vm by regex in vb
def _vm_search_by_regx(key_regx: [], verbose: VerboseType) -> str | None:
    for vm in vb_manage_command(['list', 'vms'], verbose):
        if check_string_regex(vm, key_regx):
            return vm.split(' {')[0].strip('"')
    return None


# Check is virtual machine is running
def vm_check_is_run(vm_name: str) -> bool:
    output = vb_manage_command(['showvminfo', vm_name], VerboseType.none)
    for line in output:
        if 'State' in line and 'running' in line:
            return True
    return False


# Run command for VBoxManage
def vb_manage_command(
        args: [],
        verbose: VerboseType,
        error_regx: [] = None,
        callback: Callable[[str], None] = None
) -> []:
    return pc_command([VM_MANAGE] + args, verbose, error_regx, True, callback)
