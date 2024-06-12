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

import unittest

from click.testing import CliRunner

from aurora_cli.src.base.utils.disk_cache import disk_cache_clear
from aurora_cli.src.cli.group_sdk import group_sdk


# noinspection PyTypeChecker
class TestGroupSdk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        disk_cache_clear()

    def test_sdk_a1_available(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_sdk, args=[
            'available',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('5.1.0', result.output)


if __name__ == '__main__':
    unittest.main()
