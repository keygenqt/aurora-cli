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
import shutil
from pathlib import Path

import click
from PIL import Image

from aurora_cli.src.support.output import echo_stderr, echo_stdout
from aurora_cli.src.support.texts import AppTexts


@click.group(name='icons', invoke_without_command=True)
@click.option('-p', '--path', type=click.STRING, required=True, help='Path to image')
def group_flutter_icons(path: str):
    """Gen multiple size icons for application."""

    try:
        image = Image.open(path)
    except FileNotFoundError:
        echo_stderr(AppTexts.file_not_found(path))
        exit(1)

    sizes = [
        [172, 172],
        [128, 128],
        [108, 108],
        [86, 86],
    ]

    width, height = image.size

    if width != height:
        if not click.confirm(AppTexts.confirm_image_size()):
            exit(0)

    if width < sizes[0][0] or height < sizes[0][1]:
        echo_stderr(AppTexts.error_size_image_icon(sizes[0][0], sizes[0][1]))
        exit(1)

    folder = Path(os.path.dirname(path)) / 'icons'

    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir()

    for size in sizes:
        out = Image.new('RGBA', (size[0], size[1]), (0, 0, 0, 0))
        image.thumbnail((size[0], size[1]))
        x = (out.width - image.width) // 2
        y = (out.height - image.height) // 2
        out.paste(image, (x, y))
        out.save(folder / '{}x{}.png'.format(size[0], size[1]))

    echo_stdout(AppTexts.flutter_icons_create_success(str(folder.absolute())))
