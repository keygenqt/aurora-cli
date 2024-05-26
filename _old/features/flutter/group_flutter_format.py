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
import time
from pathlib import Path

import click
from aurora_cli.src.features.flutter.impl.utils import get_list_flutter_installed
from aurora_cli.src.support.conf import URL_CLANG_FORMAT_CONF
from aurora_cli.src.support.dependency_required import check_dependency_clang_format
from aurora_cli.src.support.helper import pc_command, prompt_index, get_request, get_format_path
from aurora_cli.src.support.output import echo_stderr, echo_stdout, VerboseType
from aurora_cli.src.support.texts import AppTexts

from aurora_cli.src.base.texts.app_argument import TextArgument


@click.group(name='format', invoke_without_command=True)
@click.pass_context
@click.option('-p', '--path', type=click.STRING, default=None, required=False, help='Path to project')
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def group_flutter_format(ctx: {}, path: str, verbose: bool):
    """Formatting a C++ & Dart code project."""

    # Conf clang-format
    clang_format_path = ctx.obj.get_folder() / 'clang-format.txt'

    # Check verbose
    verbose = ctx.obj.get_type_output(verbose)

    # Required dart
    versions = get_list_flutter_installed()
    if not versions:
        echo_stderr(AppTexts.flutter_not_found())
        exit(0)

    # Check path
    if not path:
        path = './'

    # Get path application
    application_path = Path(get_format_path(path))
    if not application_path.is_dir():
        echo_stderr(AppTexts.dir_not_found(path))
        exit(0)

    # C++

    # Required dependency
    check_dependency_clang_format()

    if not os.path.isfile(clang_format_path):
        if click.confirm(AppTexts.conf_download_clang_format_conf_confirm()):
            echo_stdout(AppTexts.loading())
            # Download
            clang_conf = get_request(URL_CLANG_FORMAT_CONF)
            with open(clang_format_path, 'wb') as file:
                file.write(clang_conf.content)
        else:
            echo_stderr(AppTexts.configuration_clang_format_not_found())
            exit(0)

    files_format_count = 0
    start_format = time.time()

    # Run format C++
    if verbose != VerboseType.verbose:
        echo_stdout(AppTexts.run_clang_format(str(application_path)))

    files_format = []
    files_format.extend(application_path.rglob('*.h'))
    files_format.extend(application_path.rglob('*.cpp'))

    for file_path in files_format:
        if '/build/' in str(file_path):
            continue
        if '/3rdpatry/' in str(file_path):
            continue
        files_format_count += 1
        pc_command([
            'clang-format',
            '--style=file:{}'.format(clang_format_path),
            '-i',
            str(file_path)
        ], VerboseType.none if verbose == VerboseType.short else verbose)

    # Dart

    # Select dart
    echo_stdout(AppTexts.select_versions(versions))
    echo_stdout(AppTexts.array_indexes(versions), 2)
    dart = Path.home() / '.local' / 'opt' / 'flutter-{}'.format(versions[prompt_index(versions)]) / 'bin' / 'dart'

    # Run format Dart
    if verbose != VerboseType.verbose:
        echo_stdout(AppTexts.run_dart_format(str(application_path)))
    pc_command([
        str(dart),
        'format',
        '--line-length=120',
        str(application_path),
    ], VerboseType.none if verbose == VerboseType.short else verbose)

    if files_format and verbose != VerboseType.verbose:
        files_format_count += len([application_path.rglob('*.dart')])
        echo_stdout(AppTexts.end_format(files_format_count, f'{time.time() - start_format:.2f}'))
