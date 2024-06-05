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

from aurora_cli.src.cli.group_emulator import group_emulator
from test.set_up.set_up import emulator_off


# noinspection PyTypeChecker
class TestGroupEmulatorCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        emulator_off()

    @classmethod
    def tearDownClass(cls):
        emulator_off()

    def test_emulator_a1_start(self):
        sleep(8)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'start',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('started successfully', result.output)

    def test_emulator_a2_screenshot(self):
        sleep(8)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'screenshot',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('taken successfully', result.output)

    def test_emulator_a3_recording(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, input='', args=[
            'recording',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('recording activated', result.output)
        self.assertIn('has stopped', result.output)

    def test_emulator_a4_command_execute(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'command',
            '--execute', 'version'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Aurora', result.output)

    def test_emulator_a5_command_execute_error(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'command',
            '--execute', 'just my command',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('bash: just: not found', result.output)

    def test_emulator_a6_command_upload(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'upload',
            '--path', Path.cwd() / 'data' / 'upload.file'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('successfully uploaded', result.output)

    def test_emulator_a7_command_install(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'package-install',
            '--path', Path.cwd() / 'data' / 'com.keygenqt.trex-0.1.0-1.x86_64.rpm'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('installed successfully', result.output)

    def test_emulator_a8_command_remove(self):
        sleep(2)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'package-remove',
            '--package', 'com.keygenqt.trex'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('successfully removed', result.output)

    def test_emulator_a9_command_install_apm(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'package-install',
            '--path', Path.cwd() / 'data' / 'com.keygenqt.trex-0.1.0-1.x86_64.rpm',
            '--apm'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('installed successfully', result.output)

    def test_emulator_b1_command_remove_apm(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'package-remove',
            '--package', 'com.keygenqt.trex',
            '--apm'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('successfully removed', result.output)


if __name__ == '__main__':
    unittest.main()
