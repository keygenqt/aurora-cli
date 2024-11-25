#!/usr/bin/python3

from aurora_cli.src.api.group_api import aurora_cli_api


def main():
    result = aurora_cli_api('/app/info')
    print('Version connect Aurora CLI: {}'.format(result['value']['VERSION']))


if __name__ == '__main__':
    main()
