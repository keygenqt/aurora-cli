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

import re


def str_clear_line(line: str) -> str:
    line = line.strip()
    line = str(re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]').sub('', line))
    # I don't know how to humanely clear a line from this ***
    line = str(re.sub(r'\u0000|\u001b8|\u001b7', '', line))
    line = str(re.sub(r'\s+', ' ', line))
    return line
