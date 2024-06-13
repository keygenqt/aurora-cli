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


def percent_start(
        percents: [],
        progress: Callable[[int], None]
):
    if not percents:
        percents.append(0)
        percents.append(1)
        progress(0)
        progress(1)


def percent_end(
        percents: [],
        progress: Callable[[int], None]
):
    if 100 not in percents:
        percents.append(100)
        progress(100)


def percent_counter(
        count: int,
        percents: [],
        progress: Callable[[int], None]
):
    percent_start(percents, progress)

    if len(percents) == count + 1:
        progress(100)
        percents.append(100)
    else:
        percent = int(len(percents) * 100 / (count + 1))
        if percent not in percents and percent < 100:
            progress(percent)
        percents.append(percent)


def percent_point(
        out: str,
        points: [],
        percents: [],
        progress: Callable[[int], None]
):
    percent_start(percents, progress)

    for point in points:
        if point in out:
            if len(percents) == len(points) + 1:
                progress(100)
                percents.append(100)
            else:
                percent = int(len(percents) * 100 / (len(points) + 1))
                if percent not in percents and percent < 100:
                    progress(percent)
                percents.append(percent)
            break
