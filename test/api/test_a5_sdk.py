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

from aurora_cli.src.api.group_api import group_api
from aurora_cli.src.base.utils.disk_cache import disk_cache_clear


# noinspection PyTypeChecker
class TestSdkAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        disk_cache_clear()

    def test_sdk_a1_available(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/sdk/available'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)


if __name__ == '__main__':
    unittest.main()
