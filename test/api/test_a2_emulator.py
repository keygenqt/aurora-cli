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

from aurora_cli.src.api.group_api import group_api
from aurora_cli.src.base.utils.cache_settings import cache_settings_clear
from test.set_up.set_up import emulator_off


# noinspection PyTypeChecker
class TestEmulatorAPI(unittest.TestCase):
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
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/emulator/start'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_emulator_a2(self):
        sleep(8)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/emulator/screenshot'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('successfully', result.output)

    def test_emulator_a3(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/emulator/recording/start'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_emulator_a4(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/emulator/recording/stop'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_emulator_a5(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/emulator/command?execute=version'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('Aurora', result.output)

    def test_emulator_a6(self):
        sleep(1)
        runner = CliRunner()
        path = Path(__file__).parent.parent / 'data' / 'upload.file'
        result = runner.invoke(cli=group_api, args=[
            '--route',
            f'/emulator/upload?path={path}'
        ])
        self.assertIn('"code": 200', result.output)
        self.assertIn('successfully', result.output)

    def test_emulator_a7(self):
        sleep(1)
        runner = CliRunner()
        path = Path(__file__).parent.parent / 'data' / 'com.keygenqt.trex-0.1.0-1.x86_64.rpm'
        result = runner.invoke(cli=group_api, args=[
            '--route',
            f'/emulator/package/install?path={path}'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('successfully', result.output)

    def test_emulator_a8(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            f'/emulator/package/run?package=com.keygenqt.trex'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_emulator_a9(self):
        sleep(2)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            f'/emulator/package/remove?package=com.keygenqt.trex'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('successfully', result.output)

    def test_emulator_b1(self):
        sleep(1)
        runner = CliRunner()
        path = Path(__file__).parent.parent / 'data' / 'com.keygenqt.trex-0.1.0-1.x86_64.rpm'
        result = runner.invoke(cli=group_api, args=[
            '--route',
            f'/emulator/package/install?path={path}&apm=true'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('successfully', result.output)

    def test_emulator_b2(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            f'/emulator/package/remove?package=com.keygenqt.trex&apm=true'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('successfully', result.output)


if __name__ == '__main__':
    unittest.main()
