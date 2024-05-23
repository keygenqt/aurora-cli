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

from aurora_cli.src.cli.group_device import group_device


# noinspection PyTypeChecker
class TestGroupDeviceCLI(unittest.TestCase):
    def test_device_a1_command_execute(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            '--test',
            'command',
            '--execute', 'version'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Aurora', result.output)

    def test_device_a2_command_execute_index(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            '--test',
            'command',
            '--index', 1,
            '--execute', 'version',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Aurora', result.output)

    def test_device_a3_command_execute_select(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_device, input='1', args=[
            '--test',
            'command',
            '--select',
            '--execute', 'version',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Aurora', result.output)

    def test_device_a4_command_execute_select_index(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            '--test',
            'command',
            '--select',
            '--index', 1,
            '--execute', 'version',
        ])
        self.assertEqual(result.exit_code, 1)
        self.assertIn('Select one thing', result.output)

    def test_device_a5_command_execute_error(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            '--test',
            'command',
            '--execute', 'just my command',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('bash: just: not found', result.output)

    def test_device_a6_command_upload(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            '--test',
            'upload',
            '--path', Path.cwd() / 'data' / 'upload.file'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('successfully uploaded', result.output)

    def test_device_a7_command_install(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            '--test',
            'package-install',
            '--path', Path.cwd() / 'data' / 'com.keygenqt.trex-0.1.0-1.armv7hl.rpm'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('installed successfully', result.output)

    def test_device_a8_command_run(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            '--test',
            'package-run',
            '--package', 'com.keygenqt.trex',
            '--close'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('run successfully', result.output)

    def test_device_a9_command_remove(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_device, args=[
            '--test',
            'package-remove',
            '--package', 'com.keygenqt.trex'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('successfully removed', result.output)


if __name__ == '__main__':
    unittest.main()
