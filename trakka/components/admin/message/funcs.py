from io import BufferedReader
import json
import typing as t

import click

from trakka.utils.api import api_patch
from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.option_utils import create_option
from trakka.utils.paths import MESSAGES_PATH

def opt_queue_name(**attrs: t.Any):
    defaults = {
        'required': True,
        'help': 'Message queue name'}
    return create_option(
        "--queue",
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


def metrics_message(queue_name: str, out_format: str):
    call_get_and_print(
        f'{MESSAGES_PATH}/Metrics/{queue_name}',
        out_format,
    )


def show_message(queue_name: str, msg_id: int, out_format: str):
    call_get_and_print(
        f'{MESSAGES_PATH}/Queue/{queue_name}/{msg_id}',
        out_format,
    )


def list_message(queue_name: str, out_format: str):
    call_get_and_print(
        f'{MESSAGES_PATH}/Queue/{queue_name}',
        out_format,
    )
