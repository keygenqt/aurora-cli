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

from aurora_cli.src.base.utils.cache_func import cache_func_clear
from aurora_cli.src.base.utils.cache_settings import cache_settings_clear
from aurora_cli.src.cli.psdk.group_psdk import group_psdk
from aurora_cli.src.cli.psdk.subgroup_psdk_package import subgroup_psdk_package
from aurora_cli.src.cli.psdk.subgroup_psdk_project import subgroup_psdk_project
from aurora_cli.src.cli.psdk.subgroup_psdk_sudoers import subgroup_psdk_sudoers


# noinspection PyTypeChecker
class TestPsdkCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cache_func_clear()
        cache_settings_clear()

    def test_psdk_a1_available(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_psdk, args=[
            'available',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('5.1.0', result.output)

    def test_psdk_a1(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_psdk, args=[
            'installed',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Installed versions', result.output)

    def test_psdk_a2(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_psdk, args=[
            'targets',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_a3(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_psdk, args=[
            'install',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_a4(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_psdk, args=[
            'remove',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_a5(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_psdk, args=[
            'clear',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_a6(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_package, args=[
            'search',
            '--package', 'com.domain.app'
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_a7(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_package, args=[
            'install',
            '--path', '/home'
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_a8(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_package, args=[
            'remove',
            '--package', 'com.domain.app'
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_a9(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_package, args=[
            'validate',
            '--path', '/home'
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_b1(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_package, args=[
            'sign',
            '--path', '/home'
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_b2(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_project, args=[
            'format',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_b3(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_project, args=[
            'build',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_b4(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_project, args=[
            'icons',
            '--image', '/path/image.png'
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_b5(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_sudoers, args=[
            'add',
        ])
        self.assertEqual(result.exit_code, 0)

    def test_psdk_b6(self):
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_psdk_sudoers, args=[
            'remove',
        ])
        self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
