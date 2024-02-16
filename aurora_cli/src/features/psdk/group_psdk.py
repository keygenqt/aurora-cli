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

from aurora_cli.src.features.psdk.group_psdk_available import psdk_available
from aurora_cli.src.features.psdk.group_psdk_install import psdk_install
from aurora_cli.src.features.psdk.group_psdk_installed import psdk_installed
from aurora_cli.src.features.psdk.group_psdk_package import psdk_package_install, psdk_package_remove, \
    psdk_package_search
from aurora_cli.src.features.psdk.group_psdk_remove import psdk_remove
from aurora_cli.src.features.psdk.group_psdk_sign import psdk_sign
from aurora_cli.src.features.psdk.group_psdk_sudoers import psdk_sudoers
from aurora_cli.src.features.psdk.group_psdk_targets import psdk_list_targets
from aurora_cli.src.features.psdk.group_psdk_validate import psdk_validate


@click.group(name='psdk')
def group_psdk():
    """Working with the Aurora Platform SDK."""
    pass


# Add subgroup
group_psdk.add_command(psdk_available)
group_psdk.add_command(psdk_install)
group_psdk.add_command(psdk_installed)
group_psdk.add_command(psdk_package_install)
group_psdk.add_command(psdk_package_remove)
group_psdk.add_command(psdk_package_search)
group_psdk.add_command(psdk_remove)
group_psdk.add_command(psdk_sign)
group_psdk.add_command(psdk_sudoers)
group_psdk.add_command(psdk_list_targets)
group_psdk.add_command(psdk_validate)
