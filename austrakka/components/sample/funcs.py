from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_patch, api_get
from austrakka.utils.paths import SAMPLE_PATH
from austrakka.utils.helpers.groups import format_group_dto_for_output

DISABLE = 'Disable'
ENABLE = 'Enable'
UNSHARE = 'UnShare'
SHARE = 'Share'
GROUPS = 'Groups'


@logger_wraps()
def share_sample(
        sample_ids: [str],
        group_name: str
):
    api_patch(
        path="/".join([SAMPLE_PATH, SHARE]),
        data={
            "seqIds": sample_ids,
            "groupName": group_name
        },
    )


@logger_wraps()
def unshare_sample(
        sample_ids: [str],
        group_name: str
):
    api_patch(
        path="/".join([SAMPLE_PATH, UNSHARE]),
        data={
            "seqIds": sample_ids,
            "groupName": group_name
        },
    )


@logger_wraps()
def get_groups(
        sample_id: str,
        out_format
):
    data = api_get(path=f"{SAMPLE_PATH}/{sample_id}/{GROUPS}")['data']
    format_group_dto_for_output(data, out_format)

@logger_wraps()
def disable_sample(
        sample_ids: [str]
):
    api_patch(
        path="/".join([SAMPLE_PATH, DISABLE]),
        data={
            "seqIds": sample_ids
        },
    )


@logger_wraps()
def enable_sample(
        sample_ids: [str]
):
    api_patch(
        path="/".join([SAMPLE_PATH, ENABLE]),
        data={
            "seqIds": sample_ids
        },
    )
