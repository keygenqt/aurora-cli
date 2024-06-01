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

from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.argv import argv_is_test


@click.group(name='sundry', help=TextGroup.group_sundry())
@click.pass_context
def group_sundry(ctx: {}):
    if argv_is_test():
        ctx.obj = AppConfig.create_test()


@group_sundry.command(help=TextCommand.command_sundry_format_dart())
@click.option('-p', '--path', type=click.STRING, default=None, required=False,
              help=TextArgument.argument_path_to_project())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def format_dart(path: str, verbose: bool):
    print('Coming soon')


@group_sundry.command(help=TextCommand.command_sundry_format_clang())
@click.option('-p', '--path', type=click.STRING, default=None, required=False,
              help=TextArgument.argument_path_to_project())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def format_clang(path: str, verbose: bool):
    print('Coming soon')


@group_sundry.command(help=TextCommand.command_sundry_image_sizes())
@click.option('-p', '--path', type=click.STRING, help=TextArgument.argument_path_to_image())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def image_sizes(path: str, verbose: bool):
    print('Coming soon')
