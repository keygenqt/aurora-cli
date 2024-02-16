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
import glob
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Callable

import click
import requests
from cffi.backend_ctypes import unicode

from aurora_cli.src.support.output import echo_stderr, echo_stdout, VerboseType
from aurora_cli.src.support.texts import AppTexts


# Check folder in home dir by name, contains file
def check_home_folder(name: str, contains_name: str, contains_file_path: str) -> bool:
    if contains_name not in name:
        return False
    if not os.path.isdir(Path.home() / name):
        return False
    if not os.path.isfile(Path.home() / name / contains_file_path):
        return False
    return True


# Check list if empty exit
def check_array_with_exit(array: [], text: str) -> []:
    if not array:
        echo_stderr(text)
        exit(1)
    return array


# Check list if empty exit
def check_empty_with_exit(obj: {}, text: str) -> {}:
    if not obj:
        echo_stderr(text)
        exit(1)
    return obj


# Get fist or None from array
def get_first_or_none(array: []) -> []:
    return array[0] if array else None


# Get by index
def get_by_index(data_map: {}, index: int) -> []:
    key = None
    value = None
    keys = data_map.keys()

    if keys and 0 <= index < len(keys):
        key = list(keys)[index]
        value = data_map[key]

    return [
        key,
        value
    ]


# Prompt index by array
def prompt_index(items: [], index: int = None) -> int:
    if len(items) == 1:
        return 0
    result = -1
    while result < 0:
        if not index:
            result = click.prompt(AppTexts.select_index(), type=int)
        else:
            result = index

        if result > len(items) or result <= 0:
            echo_stderr(AppTexts.select_index_error(result))
            result = -1
            index = None

    if index:
        echo_stdout(AppTexts.select_index_success(result))

    return result - 1


# Find file in directory
def find_path_file(extension: str, path: Path) -> Path | None:
    files = glob.glob(f'{path}/*.{extension}')
    if files:
        return Path(files[0])
    return None


# Get full path file
def get_path_file(path: str, check_exist=True) -> str | None:
    if not path:
        return None

    # Format path
    if path.startswith('~/'):
        path = os.path.expanduser(path)
    if path.startswith('./'):
        path = '{}{}'.format(os.getcwd(), path[1:])
    if path.startswith('../'):
        path = '{}/{}'.format(os.getcwd(), path)

    # Read path
    path = Path(path)

    if not check_exist:
        return str(path.absolute())

    # Check exist
    if path.is_file():
        return str(path.absolute())
    else:
        echo_stderr(AppTexts.file_not_found(str(path)))
        return None


# Get full path file
def get_path_files(paths: [], extension: str = None) -> []:
    result = []
    for path in paths:
        path = get_path_file(path)
        if path:
            if not extension or path.lower().endswith('.{}'.format(extension)):
                result.append(path)
            else:
                echo_stderr(AppTexts.file_error_extension(extension, path))
    # Return with clear duplicates
    return list(set(result))


# Check string by regex array
def check_string_regex(string: str, regex: []) -> bool:
    for reg in regex:
        if re.search(reg, string):
            return True
    return False


# Common run pc command
def pc_command(
        args: [],
        verbose: VerboseType,
        error_regx: [] = None,
        error_exit: bool = True,
        callback: Callable[[str, int], None] = None,
        is_char: bool = False
) -> []:
    is_error = False
    result = []

    def output(value: any, i: int) -> bool:
        result.append(value)
        if callback:
            callback(value, i)
        if verbose == VerboseType.verbose:
            echo_stdout(value)
        if error_regx and error_regx:
            return check_string_regex(value, error_regx)
        else:
            return False

    try:
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            index = 1
            if is_char:
                for char in iter(lambda: process.stdout.read(1), b""):
                    if not char:
                        break
                    is_error = output(char, index)
                    index += 1
            else:
                for line in iter(lambda: process.stdout.readline(), ""):
                    if not line:
                        break
                    line = unicode(line.rstrip(), "utf-8")
                    is_error = output(line, index)
                    index += 1

    except Exception as e:
        is_error = output(str(e), len(result))

    if verbose == VerboseType.command:
        if is_error:
            echo_stderr(AppTexts.command_execute_error(' '.join(args)))
        else:
            echo_stdout(AppTexts.command_execute_success(' '.join(args)))

    if verbose == VerboseType.short:
        if is_error:
            echo_stderr(AppTexts.command_execute_error_short())
        else:
            echo_stdout(AppTexts.command_execute_success_short())

    if is_error and error_exit:
        exit(1)

    return result


# Remove line from file
def clear_file_line(file: Path, search: str):
    if file.is_file():
        with open(file, 'r') as f:
            lines = f.readlines()
        with open(file, 'w') as f:
            for line in lines:
                if search not in line:
                    f.write(line)


# Request sudo permissions
def sudo_request():
    subprocess.call(['sudo', 'echo'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


# Check file sum
def check_size_file(size: int, file: Path) -> bool:
    if size <= 0:
        return False
    if file.is_file():
        file_stats = os.stat(file)
        if file_stats.st_size == size:
            return True
    return False


# Get file size by url
def get_file_size(url: str) -> int:
    response = requests.head(url)
    if response.status_code == 200:
        return int(response.headers.get('content-length'))
    return -1


# Gen file name
def gen_file_name(before: str, extension: str) -> str:
    return '{before}{time}.{extension}'.format(
        before=before,
        time=datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
        extension=extension
    )
