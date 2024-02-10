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
from pathlib import Path


# Get list installed flutter
def get_list_flutter_installed() -> []:
    path = Path.home() / '.local' / 'opt'
    folders = [folder for folder in os.listdir(path) if os.path.isdir(path / folder)
               and 'flutter-' in folder
               and os.path.isfile(path / folder / 'bin' / 'flutter')]
    folders.sort(reverse=True)
    return [v.replace('flutter-', '') for v in folders]
