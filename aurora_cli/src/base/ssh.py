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
import click


# Exec command ssh
def ssh_client_exec_command(client, exec_command):
    # Exec
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(exec_command)

    title = True
    stdout = []
    stderr = []

    if ' | ' in exec_command:
        exec_command = exec_command.split(' | ')[1]

    # Output success
    for line in iter(ssh_stdout.readline, ""):
        if title:
            stdout.append('{} "{}" {}'.format(click.style('Command', fg='green'),
                                              exec_command,
                                              click.style('completed successfully:', fg='green')))
            title = False
        if 'Password' not in line:
            stdout.append(line.strip())

    # Output errors
    for line in iter(ssh_stderr.readline, ""):
        if title:
            stderr.append('{} "{}" {}'.format(click.style('Command', fg='red'),
                                              exec_command,
                                              click.style('was executed with an error:', fg='red')))
            title = False
        if 'Password' not in line:
            stderr.append(line.strip())

    return [
        '\n'.join(stdout).strip(),
        '\n'.join(stderr).strip(),
    ]
