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

from enum import Enum

import click
from bs4 import BeautifulSoup


class EchoTextStyles(Enum):
    i = 'i'
    u = 'u'
    d = 'd'
    t = 't'


class EchoTextColors(Enum):
    red = 'red'
    green = 'green'
    yellow = 'yellow'
    blue = 'blue'
    magenta = 'magenta'
    cyan = 'cyan'
    white = 'white'
    reset = 'reset'
    hint = 'hint'


# Colorize text clear
def text_colorize_clear(text: str) -> str:
    if '<' not in text:
        return text
    soup = BeautifulSoup(text, 'html.parser')
    for tag in EchoTextStyles:
        for item in soup.findAll(tag.value):
            text = text.replace('<{}>{}</{}>'.format(tag.value, item.text, tag.value), item.text)
    soup = BeautifulSoup(text, 'html.parser')
    for tag in EchoTextColors:
        for item in soup.findAll(tag.value):
            text = text.replace('<{}>{}</{}>'.format(tag.value, item.text, tag.value), item.text)
    return text


# Colorize text by tags
def text_colorize(text: str) -> str:
    if '<' not in text:
        return text

    soup = BeautifulSoup(text, 'html.parser')
    for tag in EchoTextStyles:
        for item in soup.findAll(tag.value):
            is_italic = False
            is_underline = False
            is_dim = False
            if tag == EchoTextStyles.i:
                is_italic = True
            if tag == EchoTextStyles.u:
                is_underline = True
            if tag == EchoTextStyles.d:
                is_dim = True
            if tag == EchoTextStyles.t:
                is_italic = True
                is_dim = True

            text = text.replace(
                '<{}>{}</{}>'.format(tag.value, item.text, tag.value),
                click.style(item.text, italic=is_italic, underline=is_underline, dim=is_dim))

    soup = BeautifulSoup(text, 'html.parser')
    for tag in EchoTextColors:
        for item in soup.findAll(tag.value):
            text = text.replace(
                '<{}>{}</{}>'.format(tag.value, item.text, tag.value),
                click.style(item.text, fg='reset' if tag == EchoTextColors.hint else tag.value))

    return click.style(text, fg='reset')


def text_multiline_help(text: str) -> str:
    out = []
    for line in text.split('\n'):
        if len(line.strip()) == 0:
            out.append('\b')
        else:
            out.append(line.replace(' ', ' ') + str(' ' * (62 - len(line))))
    return '\n'.join(out)
