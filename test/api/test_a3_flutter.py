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
class TestFlutterAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cache_func_clear()
        cache_settings_clear()

    def test_flutter_a1(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/flutter/available'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_flutter_a2(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/flutter/installed'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_flutter_a3(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/flutter/install?version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_flutter_a4(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/flutter/remove?version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_flutter_a5(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/flutter/project/format?version=1&path=/home'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_flutter_a6(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/flutter/project/report?version=1&path=/home'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_flutter_a7(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/flutter/project/icons?image=/image.png&path=/home'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_flutter_a8(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/flutter/project/build?target=1&path=/home&flutter_version=1&psdk_version=1&key_name=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)


if __name__ == '__main__':
    unittest.main()
