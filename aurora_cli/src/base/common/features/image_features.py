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

from pathlib import Path
from typing import Any

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import OutResult, OutResultError


def image_crop_for_project(
        path_image: Path,
        path_folder: Path,
        app_qt_id: Any = None
) -> OutResult:
    from PIL import Image

    sizes = [
        [172, 172],
        [128, 128],
        [108, 108],
        [86, 86],
    ]

    if not path_image.is_file():
        return OutResultError(TextError.file_not_found_error(str(path_image)))
    try:
        image = Image.open(path_image)
    except (Exception,):
        return OutResultError(TextError.file_read_error(str(path_image)))

    width, height = image.size

    if width < sizes[0][0] or height < sizes[0][1]:
        return OutResultError(TextError.image_size_icon_error(sizes[0][0], sizes[0][1]))

    path_folder.mkdir(parents=True, exist_ok=True)

    for size in sizes:
        out = Image.new('RGBA', (size[0], size[1]), (0, 0, 0, 0))
        image.thumbnail((size[0], size[1]))
        x = (out.width - image.width) // 2
        y = (out.height - image.height) // 2
        out.paste(image, (x, y))
        if app_qt_id:
            path_save = path_folder / '{}x{}'.format(size[0], size[1])
            path_save.mkdir(parents=True, exist_ok=True)
            out.save(path_save / '{}.png'.format(app_qt_id))
        else:
            out.save(path_folder / '{}x{}.png'.format(size[0], size[1]))

    return OutResult(TextSuccess.image_resize_success(str(path_folder)), value=path_folder)
