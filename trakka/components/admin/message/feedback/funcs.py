from trakka.utils.api import api_delete
from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.paths import MESSAGES_PATH


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
