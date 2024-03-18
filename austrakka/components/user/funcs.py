from typing import List
import pandas as pd

from austrakka.utils.api import api_get
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.api import api_patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import USER_PATH
from austrakka.utils.output import print_formatted


@logger_wraps()
def list_users(show_disabled: bool, out_format: str):
    response = api_get(
        path=USER_PATH,
        params={
            'includeall': show_disabled
        }
    )

    data = response['data'] if ('data' in response) else response
    pd.set_option('display.max_rows', 500)
    urg = pd.json_normalize(data, record_path='userRoleGroup') \
        .pipe(lambda x: x.drop('role.id', axis=1)) \
        .pipe(lambda x: x.drop('group.id', axis=1))

    org = pd.json_normalize(data)\
        .pipe(lambda x: x.drop('lastUpdatedBy', axis=1))\
        .pipe(lambda x: x.drop('lastUpdated', axis=1))\
        .pipe(lambda x: x.drop('created', axis=1))\
        .pipe(lambda x: x.drop('userRoleGroup', axis=1))\
        .pipe(lambda x: x.drop('organisation.id', axis=1))\
        .pipe(lambda x: x.drop('createdBy', axis=1))

    normalized = pd.merge(
        urg,
        org,
        how="inner",
        on=None,
        left_on="user.userId",
        right_on="userId",
        left_index=False,
        right_index=False,
        sort=True,
        suffixes=("_x", "_y"),
        copy=True,
        indicator=False,
        validate=None,
    )\
        .sort_values(["user.userId", "isAusTrakkaAdmin", "group.name"]) \
        .pipe(lambda x: x.drop('userId', axis=1))

    print_formatted(
        normalized,
        out_format,
    )


@logger_wraps()
def add_user(
    user_id: str,
    org: str,
    owner_group_roles: List[str],
    is_austrakka_process: bool,
):
    user = {
        "objectId": user_id,
        "organisation": {
            "abbreviation": org
        },
        "ownerGroupRoles": list(owner_group_roles),
        "isAusTrakkaProcess": is_austrakka_process,
    }

    api_post(
        path=USER_PATH,
        data=user
    )


@logger_wraps()
def update_user(
    user_id: int,
    org: str,
    owner_group_roles: List[str],
    is_austrakka_process: bool,
):
    user = {
        "organisation": {
            "abbreviation": org
        },
        "ownerGroupRoles": list(owner_group_roles),
        "isAusTrakkaProcess": is_austrakka_process,
    }

    api_put(
        path=f'{USER_PATH}/{user_id}',
        data=user
    )


@logger_wraps()
def enable_user(user_id: str):
    api_patch(path=f'{USER_PATH}/enable/{user_id}')


@logger_wraps()
def disable_user(user_id: str):
    api_patch(path=f'{USER_PATH}/disable/{user_id}')
