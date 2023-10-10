import pandas as pd
from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_patch, api_get
from austrakka.utils.paths import SAMPLE_PATH
from austrakka.utils.output import print_table


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
    result = pd.json_normalize(data, max_level=1)

    if 'organisation' in result.columns:
        result.drop(['organisation'],
                    axis='columns',
                    inplace=True)

    result.fillna('', inplace=True)
    print_table(result, out_format)

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
