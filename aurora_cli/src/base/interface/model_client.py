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

from abc import abstractmethod
from pathlib import Path
from typing import Any


# Interface for model classes with ssh client
class ModelClient:
    @abstractmethod
    def get_ssh_client(self):
        pass

    @abstractmethod
    def get_pass(self) -> Any:
        pass

    @abstractmethod
    def get_host(self) -> str:
        pass

    @abstractmethod
    def get_port(self) -> int:
        pass

    @abstractmethod
    def get_ssh_key(self) -> Any:
        pass

    @abstractmethod
    def is_password(self) -> bool:
        pass
