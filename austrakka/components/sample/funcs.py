from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_patch, api_get
from austrakka.utils.paths import SAMPLE_PATH
from austrakka.utils.helpers.groups import format_group_dto_for_output
from austrakka.utils.helpers.output import call_get_and_print

DISABLE = 'Disable'
ENABLE = 'Enable'
UNSHARE = 'UnShare'
SHARE = 'Share'
GROUPS = 'Groups'
PURGE = 'Purge'


@logger_wraps()
def show_sample(
        seq_id: str,
        out_format: str,
):
    call_get_and_print(
        path="/".join([SAMPLE_PATH, seq_id]),
        out_format=out_format
    )


@logger_wraps()
def share_sample(
        seq_ids: [str],
        group_name: str
):
    api_patch(
        path="/".join([SAMPLE_PATH, SHARE]),
        data={
            "seqIds": seq_ids,
            "groupName": group_name
        },
    )


@logger_wraps()
def unshare_sample(
        seq_ids: [str],
        group_name: str
):
    api_patch(
        path="/".join([SAMPLE_PATH, UNSHARE]),
        data={
            "seqIds": seq_ids,
            "groupName": group_name
        },
    )


@logger_wraps()
def get_groups(
        seq_id: str,
        out_format
):
    data = api_get(path=f"{SAMPLE_PATH}/{seq_id}/{GROUPS}")['data']
    format_group_dto_for_output(data, out_format)

@logger_wraps()
def disable_sample(
        seq_ids: [str]
):
    api_patch(
        path="/".join([SAMPLE_PATH, DISABLE]),
        data={
            "seqIds": seq_ids
        },
    )


@logger_wraps()
def enable_sample(
        seq_ids: [str]
):
    api_patch(
        path="/".join([SAMPLE_PATH, ENABLE]),
        data={
            "seqIds": seq_ids
        },
    )


@logger_wraps()
def purge_sample(
        seq_id: str
):
    api_patch(
        path="/".join([SAMPLE_PATH, seq_id, PURGE]),
    )
