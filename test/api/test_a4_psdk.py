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
class TestPsdkAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cache_func_clear()
        cache_settings_clear()

    def test_psdk_a1(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/available'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_a2(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/installed'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_a3(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/targets?version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_a4(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/install?version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_a5(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/remove?version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_a6(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/clear?version=1&target=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_a7(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/sudoers/add?version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_a8(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/sudoers/remove?version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_a9(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/package/search?target=1&package=1&version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_b1(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/package/install?target=1&path=1&version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_b2(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/package/remove?target=1&package=1&version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_b3(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/package/validate?target=1&path=1&profile=1&version=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_b4(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/package/sign?path=1&version=1&key=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_b5(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/project/format?path=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_b6(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/project/icons?path=1&image=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_psdk_b7(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/psdk/project/build?target=1&path=1&version=1&name=1'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)


if __name__ == '__main__':
    unittest.main()
