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

from aurora_cli.src.features.psdk.impl.utils import get_psdk_installed_versions
from aurora_cli.src.support.output import echo_stdout, echo_stderr
from aurora_cli.src.support.texts import AppTexts


@click.group(name='installed', invoke_without_command=True)
def psdk_installed():
    """Get installed list Aurora Platform SDK."""

    versions = get_psdk_installed_versions()

    if versions:
        echo_stdout(AppTexts.psdk_installed_versions(versions))
    else:
        echo_stderr(AppTexts.psdk_not_found())
