from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import patch
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
    call_api(
        method=patch,
        path="/".join([SAMPLE_PATH, SHARE]),
        body={
            "seqIds": sample_ids,
            "groupName": group_name
        },
    )


@logger_wraps()
def unshare_sample(
        sample_ids: [str],
        group_name: str
):
    call_api(
        method=patch,
        path="/".join([SAMPLE_PATH, UNSHARE]),
        body={
            "seqIds": sample_ids,
            "groupName": group_name
        },
    )


@logger_wraps()
def disable_sample(
        sample_ids: [str]
):
    call_api(
        method=patch,
        path="/".join([SAMPLE_PATH, DISABLE]),
        body={
            "seqIds": sample_ids
        },
    )


@logger_wraps()
def enable_sample(
        sample_ids: [str]
):
    call_api(
        method=patch,
        path="/".join([SAMPLE_PATH, ENABLE]),
        body={
            "seqIds": sample_ids
        },
    )
