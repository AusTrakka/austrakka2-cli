from austrakka.utils.api import api_delete
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.paths import MESSAGES_PATH


def show_feedback(msg_id: int, out_format: str):
    call_get_and_print(
        f'{MESSAGES_PATH}/Feedback/{msg_id}',
        out_format,
    )


def list_feedback(out_format: str):
    call_get_and_print(
        f'{MESSAGES_PATH}/Feedback',
        out_format,
    )


def delete_feedback(msg_id: int):
    api_delete(
        f'{MESSAGES_PATH}/Feedback/{msg_id}'
    )


