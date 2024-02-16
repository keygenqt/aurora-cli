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

from aurora_cli.src.support.output import echo_stdout
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.versions import get_versions_sdk


@click.group(name='available', invoke_without_command=True)
def psdk_available():
    """Get available version Aurora Platform SDK."""

    versions = get_versions_sdk()

    echo_stdout(AppTexts.psdk_versions(versions))
