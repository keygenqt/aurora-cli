import os

import paramiko

from app.src.base.sdk import get_sdk_installed


# Get ssh client emulator
def get_ssh_client_vm(is_root=False):
    _, path = get_sdk_installed()
    if not path:
        return None
    try:
        key_path = '{}{}'.format(path, '/vmshare/ssh/private_keys/sdk')
        username = 'root' if is_root else 'defaultuser'
        # Connect
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('localhost', username=username, key_filename=key_path, timeout=5, port=2223)
        return client
    except paramiko.ssh_exception.SSHException:
        pass
    except paramiko.ssh_exception.NoValidConnectionsError:
        pass
    except TimeoutError:
        pass
    return None


# Upload file
def upload_file_sftp_vm(upload_path, file_path, is_root=False):
    client = get_ssh_client_vm(is_root)
    if not client:
        return None
    try:
        # Get file name
        file_name = os.path.basename(file_path)
        # Upload file
        client.open_sftp().put(file_path, '{upload_path}/{file_name}'.format(
            upload_path=upload_path,
            file_name=file_name
        ))
        client.close()
    except paramiko.ssh_exception.SSHException:
        return False
    except FileNotFoundError:
        return False
    return True
