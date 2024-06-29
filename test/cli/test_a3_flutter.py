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
from pathlib import Path

from click.testing import CliRunner

from aurora_cli.src.base.utils.cache_func import cache_func_clear
from aurora_cli.src.base.utils.cache_settings import cache_settings_clear
from aurora_cli.src.cli.flutter.group_flutter import group_flutter
from aurora_cli.src.cli.flutter.subgroup_flutter_project import subgroup_flutter_project


# noinspection PyTypeChecker
class TestFlutterCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cache_func_clear()
        cache_settings_clear()

    def test_flutter_a1(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_flutter, args=[
            'available',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('3.16.2-2', result.output)

    def test_flutter_a2(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_flutter, args=[
            'installed',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_flutter_a3(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_flutter, args=[
            'install',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_flutter_a4(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_flutter, args=[
            'remove',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_flutter_a5(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_flutter, input='', args=[
            'custom-devices',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Are you ready to continue?', result.output)

    def test_flutter_a6(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_flutter_project, args=[
            'format',
            '--path', Path(__file__).parent
        ])
        self.assertEqual(result.exit_code, 0)

    def test_flutter_a7(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_flutter_project, args=[
            'report',
            '--path', Path(__file__).parent
        ])
        self.assertEqual(result.exit_code, 0)

    def test_flutter_a8(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_flutter_project, args=[
            'icons',
            '--image', '/path/to/error/image.png'
        ])
        self.assertEqual(result.exit_code, 0)

    def test_flutter_a9(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_flutter_project, args=[
            'build',
        ])
        self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
