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

from aurora_cli.src.features.flutter.group_flutter_debug_dart import group_flutter_debug_dart
from aurora_cli.src.features.flutter.group_flutter_debug_gdb import group_flutter_debug_gdb


@click.group(name='debug')
def group_flutter_debug():
    """Debug project Flutter SDK for Aurora OS."""
    pass


# Add subgroup
group_flutter_debug.add_command(group_flutter_debug_dart)
group_flutter_debug.add_command(group_flutter_debug_gdb)
