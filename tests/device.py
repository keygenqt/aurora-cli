import unittest

from click.testing import CliRunner

from aurora_cli.src.cli.device import group_device


# noinspection PyTypeChecker
class TestGroupDevices(unittest.TestCase):
    def test_command_execute(self):
        runner = CliRunner()
        result = runner.invoke(group_device, [
            '--test',
            'command',
            '--execute',
            'version',
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Aurora', result.output)


if __name__ == '__main__':
    unittest.main()
