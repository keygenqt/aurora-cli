import paramiko


# Get ssh clients available devices
# This allows you to select only those devices that are available
def get_ssh_clients(devices):
    # Check ssh connect
    clients = {}
    for ip, values in devices.items():
        client = get_ssh_client(ip, values['pass'])
        if client:
            clients[ip] = client
    return clients


# Get ssh client
def get_ssh_client(ip, password):
    try:
        # Connect
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username='defaultuser', password=password)
        return client
    except paramiko.ssh_exception.SSHException:
        pass
    return None
