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


def ssh_device_command_api(execute: str, verbose: bool):
    """Execute the command on the device."""
    pass
    # echo_stdout_json(ssh_command(execute), verbose)


def ssh_device_run_api(package: str, verbose: bool):
    """Run package on device in container."""
    pass
    # echo_stdout_json(ssh_run(package), verbose)


def ssh_device_upload_api(path: [], verbose: bool):
    """Upload file to ~/Download directory device."""
    pass
    # echo_stdout_json(ssh_upload(path), verbose)


def ssh_device_install_api(path: [], apm: bool, verbose: bool):
    """Install RPM package on device."""
    pass
    # echo_stdout_json(ssh_install(path, apm), verbose)


def ssh_device_remove_api(package: str, apm: bool, verbose: bool):
    """Remove package from device."""
    pass
    # echo_stdout_json(ssh_remove(package, apm), verbose)
