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
from time import sleep

from click.testing import CliRunner

from aurora_cli.src.base.utils.cache_settings import cache_settings_clear
from aurora_cli.src.cli.device.group_device import group_device
from aurora_cli.src.cli.device.subgroup_device_package import subgroup_device_package


# noinspection PyTypeChecker
class TestDeviceCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cache_settings_clear()

    def test_device_a1(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            'command',
            '--execute', 'version'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Aurora', result.output)

    def test_device_a2(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            'command',
            '--index', 1,
            '--execute', 'version',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Aurora', result.output)

    def test_device_a3(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            'command',
            '--select',
            '--index', 1,
            '--execute', 'version',
        ])
        self.assertEqual(result.exit_code, 1)
        self.assertIn('Select one thing', result.output)

    def test_device_a4(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            'command',
            '--execute', 'just my command',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('bash: just: not found', result.output)

    def test_device_a5(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            'upload',
            '--path', Path(__file__).parent.parent / 'data' / 'upload.file'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('uploaded successfully', result.output)

    def test_device_a6(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_device_package, args=[
            'install',
            '--path', Path(__file__).parent.parent / 'data' / 'com.keygenqt.trex-0.1.0-1.armv7hl.rpm',
            '--apm'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('installed successfully', result.output)

    def test_device_a7(self):
        sleep(2)
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_device_package, args=[
            'remove',
            '--package', 'com.keygenqt.trex',
            '--apm'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('removed successfully', result.output)


if __name__ == '__main__':
    unittest.main()
