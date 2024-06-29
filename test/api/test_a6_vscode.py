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
from aurora_cli.src.base.utils.cache_func import cache_func_clear
from aurora_cli.src.base.utils.cache_settings import cache_settings_clear


# noinspection PyTypeChecker
class TestSdkAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cache_func_clear()
        cache_settings_clear()

    def test_sdk_a1(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/vscode/extensions/list'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_sdk_a2(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/vscode/extensions/check/flutter'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_sdk_a3(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/vscode/extensions/check/cpp'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_sdk_a4(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/vscode/extensions/check/other'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_sdk_a5(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/vscode/extensions/install?extension=test'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_sdk_a6(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/vscode/settings/update'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)


if __name__ == '__main__':
    unittest.main()
