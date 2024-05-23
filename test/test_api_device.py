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

from aurora_cli.src.api.group_api import group_api


# noinspection PyTypeChecker
class TestGroupDeviceAPI(unittest.TestCase):
    def test_device_a1_device_list(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--test',
            '--route',
            '/device/list'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('192.168.2.15', result.output)

    def test_device_a2_command_execute(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--test',
            '--route',
            '/device/ssh/command?host=192.168.2.15&port=22&auth=00000&execute=version'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Aurora', result.output)

    def test_device_a3_command_execute_error(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--test',
            '--route',
            '/device/ssh/command?host=192.168.2.15&port=22&auth=00000'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('is required', result.output)

    def test_device_a4_command_upload(self):
        runner = CliRunner()
        path = Path.cwd() / 'data' / 'upload.file'
        result = runner.invoke(cli=group_api, args=[
            '--test',
            '--route',
            f'/device/ssh/upload?host=192.168.2.15&port=22&auth=00000&path={path}'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('successfully uploaded', result.output)

    def test_device_a5_command_install(self):
        runner = CliRunner()
        path = Path.cwd() / 'data' / 'com.keygenqt.trex-0.1.0-1.armv7hl.rpm'
        result = runner.invoke(cli=group_api, args=[
            '--test',
            '--route',
            f'/device/ssh/package-install?host=192.168.2.15&port=22&auth=00000&devel_su=00000&path={path}'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('installed successfully', result.output)

    def test_device_a6_command_run(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--test',
            '--route',
            f'/device/ssh/package-run?host=192.168.2.15&port=22&auth=00000&close=true&package=com.keygenqt.trex'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('run successfully', result.output)

    def test_device_a7_command_remove(self):
        runner = CliRunner()
        result = runner.invoke(cli=group_api, args=[
            '--test',
            '--route',
            f'/device/ssh/package-remove?host=192.168.2.15&port=22&auth=00000&devel_su=00000&package=com.keygenqt.trex'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('successfully removed', result.output)


if __name__ == '__main__':
    unittest.main()
