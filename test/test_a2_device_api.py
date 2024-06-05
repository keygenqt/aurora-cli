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


# noinspection PyTypeChecker
class TestGroupDeviceAPI(unittest.TestCase):
    def test_device_a1_device_list(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/device/list'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)

    def test_device_a2_command_execute(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/device/ssh/command?host=192.168.2.15&execute=version'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('Aurora', result.output)

    def test_device_a3_command_execute_error(self):
        sleep(1)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            '/device/ssh/command?host=192.168.2.15'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 500', result.output)

    def test_device_a4_command_upload(self):
        sleep(1)
        runner = CliRunner()
        path = Path.cwd() / 'data' / 'upload.file'
        result = runner.invoke(cli=group_api, args=[
            '--route',
            f'/device/ssh/upload?host=192.168.2.15&path={path}'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('successfully', result.output)

    def test_device_a5_command_install(self):
        sleep(1)
        runner = CliRunner()
        path = Path.cwd() / 'data' / 'com.keygenqt.trex-0.1.0-1.armv7hl.rpm'
        result = runner.invoke(cli=group_api, args=[
            '--route',
            f'/device/ssh/package-install?host=192.168.2.15&path={path}&apm=true'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('successfully', result.output)

    def test_device_a6_command_remove(self):
        sleep(2)
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--route',
            f'/device/ssh/package-remove?host=192.168.2.15&package=com.keygenqt.trex&apm=true'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('"code": 200', result.output)
        self.assertIn('successfully', result.output)


if __name__ == '__main__':
    unittest.main()
