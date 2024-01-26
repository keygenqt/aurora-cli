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
import os

import click
import paramiko

from aurora_cli.src.base.utils import get_string_from_list_numbered, prompt_index


# Get ssh clients available devices
# This allows you to select only those devices that are available
def get_ssh_clients(devices, index=None):
    # Check ssh connect
    clients = {}
    i = 0
    for ip, values in devices.items():
        i += 1
        if not index:
            client = get_ssh_client(ip, values['port'], values['pass'])
            if client:
                clients[ip] = client
        else:
            if i == index:
                client = get_ssh_client(ip, values['port'], values['pass'])
                if client:
                    clients[ip] = client
                break
    return clients


# Get ssh client
def get_ssh_client(ip, port, password):
    try:
        # Connect
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username='defaultuser', password=password, port=port, timeout=5)
        return client
    except paramiko.ssh_exception.SSHException:
        pass
    except paramiko.ssh_exception.NoValidConnectionsError:
        pass
    except TimeoutError:
        pass
    return None


# Get ssh client with query
def prompt_ssh_client_device(ctx, index=None):
    devices = ctx.obj.get_devices()

    # Get connections
    clients = get_ssh_clients(devices, index)

    if not clients:
        click.echo(click.style('No active devices found', fg='red'))
        exit(1)

    if index:
        click.echo('Found devices:\n{}'
                   .format(get_string_from_list_numbered(devices.keys())))
        click.echo('\nIndex was selected: {}\n'.format(index))

    if len(clients.keys()) != 1:
        click.echo('Found active devices:\n{}'
                   .format(get_string_from_list_numbered(clients.keys())))

    # Query index
    index = prompt_index(clients.keys(), index)
    key = list(clients.keys())[index - 1]

    return [
        key,
        clients[key]
    ]


# Upload file
def upload_file_sftp(ctx, device, upload_path, file_path):
    devices = ctx.obj.get_devices()
    ip = device
    port = int(devices[device]['port'])
    password = devices[device]['pass']
    try:
        # Connect
        transport = paramiko.Transport((ip, port))
        transport.connect(username='defaultuser', password=password)
        client = paramiko.SFTPClient.from_transport(transport)
        # Get file name
        file_name = os.path.basename(file_path)
        # Upload file
        client.put(file_path, '{upload_path}/{file_name}'.format(
            upload_path=upload_path,
            file_name=file_name
        ))
        client.close()
        transport.close()
    except paramiko.ssh_exception.SSHException:
        return False
    except FileNotFoundError:
        return False
    return True
