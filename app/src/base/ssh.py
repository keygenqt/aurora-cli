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
