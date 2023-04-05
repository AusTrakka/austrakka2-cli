from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_patch
from austrakka.utils.paths import SAMPLE_PATH

DISABLE = 'Disable'
ENABLE = 'Enable'
UNSHARE = 'UnShare'
SHARE = 'Share'


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
