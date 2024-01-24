import os
import subprocess
import tempfile

import click
from alive_progress import alive_bar


# Get output string from array with indexes
def get_string_from_list_numbered(items: []):
    list_numbered = ['{}: {}'.format(index + 1, str(item)) for index, item in enumerate(items)]
    list_format = [(item[:-1] if item.endswith('/') else item) for item in list_numbered]
    return '\n'.join(list_format)


# Get output string from array
def get_string_from_list(items: []):
    list_format = [(item[:-1] if item.endswith('/') else item) for item in items]
    return '\n'.join(list_format)


# Prompt index by array
def prompt_index(items: [], index=None):
    if len(items) == 1:
        return 1
    result = -1
    while result < 0:
        if not index:
            result = click.prompt('\nSelect index', type=int)
        else:
            result = index

        if result > len(items) or result <= 0:
            click.echo(click.style(f"Error: '{result}' is not a valid index.", fg='red'), err=True)
            result = -1
            index = None

    if index:
        click.echo('\nSelect index: {}'.format(result))

    return result


# Bar for subprocess by symbol
def bar_subprocess_symbol(size, process):
    counter = 0
    with alive_bar(size) as bar:
        for _ in iter(lambda: process.stdout.read(1), b""):
            counter += 1
            if counter < size:
                bar()
        bar(size - counter)


# Bar for subprocess by lines
def bar_subprocess_lines(size, process):
    counter = 0
    with alive_bar(size) as bar:
        for out in iter(lambda: process.stdout.readline(), ""):
            if not out:
                break
            counter += 1
            if counter < size:
                bar()
        bar(size - counter)


# Move file with root permissions
def move_root_file(file_from, file_to):
    subprocess.call(['sudo', 'chmod', '644', file_from])
    subprocess.call(['sudo', 'chown', 'root:root', file_from])
    subprocess.call(['sudo', 'rm', '-rf', file_to])
    subprocess.call(['sudo', 'mv', file_from, file_to])


# Remove line from file by search contains string
def update_file_lines(file_path, search, insert=None):
    lines = []
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        # Clear record if exist
        for line in lines:
            if search not in line:
                f.write(line)
        # Insert data
        if insert:
            f.write(insert)
        return f.name


# Get full path to file
def get_full_path(path, extension=None):
    # Relative path
    if path.startswith('./'):
        path = '{}{}'.format(os.getcwd(), path[1:])

    # Check
    if os.path.isfile(path):
        if extension and not path.lower().endswith('.{}'.format(extension)):
            click.echo('{} {}'.format(click.style('The file has an incorrect extension: ', fg='red'), path), err=True)
        else:
            return path
    else:
        click.echo('{} {}'.format(click.style('File not found:', fg='red'), path), err=True)

    return None
