from io import BufferedReader
import json
import typing as t

import click

from austrakka.utils.api import api_patch
from austrakka.utils.option_utils import create_option
from austrakka.utils.paths import MESSAGES_PATH

def opt_queue_name(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Message queue name'}
    return create_option(
        "--queue-name",
        **{**defaults, **attrs}
    )


def opt_msg_id(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Message id'}
    return create_option(
        "--msg-id",
        type=click.INT,
        **{**defaults, **attrs}
    )


def add_message(file: BufferedReader, queue_name: str):
    file_json = json.loads(file.read())
    api_patch(
        f'{MESSAGES_PATH}/{queue_name}',
        data=file_json
    )
