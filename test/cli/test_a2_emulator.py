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
from aurora_cli.src.cli.emulator.group_emulator import group_emulator
from aurora_cli.src.cli.emulator.subgroup_emulator_package import subgroup_emulator_package
from test.set_up.set_up import emulator_off


# noinspection PyTypeChecker
class TestEmulatorCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        emulator_off()
        cache_settings_clear()

    @classmethod
    def tearDownClass(cls):
        emulator_off()

    def test_emulator_a1(self):
        sleep(8)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'start',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('started successfully', result.output)

    def test_emulator_a2(self):
        sleep(8)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'screenshot',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('taken successfully', result.output)

    def test_emulator_a3(self):
        sleep(8)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, input='', args=[
            'recording',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('File is saved', result.output)

    def test_emulator_a4(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'command',
            '--execute', 'version'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Aurora', result.output)

    def test_emulator_a5(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'command',
            '--execute', 'just my command',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('bash: just: not found', result.output)

    def test_emulator_a6(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_emulator, args=[
            'upload',
            '--path', Path(__file__).parent.parent / 'data' / 'upload.file'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('uploaded successfully', result.output)

    def test_emulator_a7(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_emulator_package, args=[
            'install',
            '--path', Path(__file__).parent.parent / 'data' / 'com.keygenqt.trex-0.1.0-1.x86_64.rpm'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('installed successfully', result.output)

    def test_emulator_a8(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_emulator_package, args=[
            'run',
            '--package', 'com.keygenqt.trex'
        ])
        self.assertEqual(result.exit_code, 0)

    def test_emulator_a9(self):
        sleep(2)
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_emulator_package, args=[
            'remove',
            '--package', 'com.keygenqt.trex'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('removed successfully', result.output)

    def test_emulator_b1(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_emulator_package, args=[
            'install',
            '--path', Path(__file__).parent.parent / 'data' / 'com.keygenqt.trex-0.1.0-1.x86_64.rpm',
            '--apm'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('installed successfully', result.output)

    def test_emulator_b2(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=subgroup_emulator_package, args=[
            'remove',
            '--package', 'com.keygenqt.trex',
            '--apm'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('removed successfully', result.output)


if __name__ == '__main__':
    unittest.main()
