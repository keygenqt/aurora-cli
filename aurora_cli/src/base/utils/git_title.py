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
from typing import Any

from git import RemoteProgress

from aurora_cli.src.base.localization.localization import localization_git_clone


class TitleOpCode(RemoteProgress):
    OP_CODES = [
        "BEGIN",
        "CHECKING_OUT",
        "COMPRESSING",
        "COUNTING",
        "END",
        "FINDING_SOURCES",
        "RECEIVING",
        "RESOLVING",
        "WRITING",
    ]

    OP_CODE_NAMES = {
        getattr(RemoteProgress, _op_code): _op_code for _op_code in OP_CODES
    }

    @classmethod
    def _get_title(cls, op_code: int) -> Any:
        mask = op_code & cls.OP_MASK
        for key, value in cls.OP_CODE_NAMES.items():
            if key == mask:
                return value.title()
        return None

    @staticmethod
    def get_title(op_code: int) -> str:
        return localization_git_clone(TitleOpCode()._get_title(op_code))
