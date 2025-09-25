
from austrakka.utils.api import api_delete, api_patch
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.paths import MESSAGES_PATH


def show_dl(queue_name: str, msg_id: int, out_format: str):
    call_get_and_print(
        f'{MESSAGES_PATH}/DeadLetter/{queue_name}/{msg_id}',
        out_format,
    )


def list_dl(queue_name: str, out_format: str):
    call_get_and_print(
        f'{MESSAGES_PATH}/DeadLetter/{queue_name}',
        out_format,
    )


def delete_dl(queue_name: str, msg_id: int):
    api_delete(
        f'{MESSAGES_PATH}/DeadLetter/{queue_name}/{msg_id}'
    )


def summary_dl(out_format: str):
    call_get_and_print(
        f'{MESSAGES_PATH}/DeadLetter/Summary',
        out_format,
    )


def resend_dl(queue_name: str, msg_id: int):
    api_patch(
        f'{MESSAGES_PATH}/DeadLetter/{queue_name}/{msg_id}/Resend'
    )
