from typing import List

import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.api import post
from austrakka.utils.api import put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import USER_PATH


@logger_wraps()
def list_users():
    response = call_api(
        method=get,
        path=USER_PATH,
        params={
            'includeall': False
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
        .pipe(lambda x: x.drop('userId', axis=1))\
        .pipe(lambda x: x.drop('isActive', axis=1))\
        .pipe(lambda x: x.drop('userRoleGroup', axis=1))\
        .pipe(lambda x: x.drop('organisation.id', axis=1))\
        .pipe(lambda x: x.drop('createdBy', axis=1))

    normalized = pd.merge(
        urg,
        org,
        how="inner",
        on=None,
        left_on="user.userLogin",
        right_on="userLogin",
        left_index=False,
        right_index=False,
        sort=True,
        suffixes=("_x", "_y"),
        copy=True,
        indicator=False,
        validate=None,
    )\
        .sort_values(["user.userId", "isAusTrakkaAdmin", "group.name"]) \
        .pipe(lambda x: x.drop('userLogin', axis=1))

    # pylint: disable=print-function
    print(normalized)


@logger_wraps()
def add_user(
    email: str,
    org: str,
    owner_group_roles: List[str],
):
    user = {
        "userLogin": email,
        "organisation": {
            "abbreviation": org
        },
        "ownerGroupRoles": list(owner_group_roles),
    }

    call_api(
        method=post,
        path=USER_PATH,
        body=user
    )


@logger_wraps()
def update_user(
    user_id: int,
    org: str,
    owner_group_roles: List[str],
):
    user = {
        "organisation": {
            "abbreviation": org
        },
        "ownerGroupRoles": list(owner_group_roles),
    }

    call_api(
        method=put,
        path=f'{USER_PATH}/{user_id}',
        body=user
    )
