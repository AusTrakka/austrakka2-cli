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
    urg = pd.json_normalize(data, record_path='userRoleGroup')
    org = pd.json_normalize(data)\
        .pipe(lambda x: x.drop('lastUpdatedBy', 1))\
        .pipe(lambda x: x.drop('lastUpdated', 1))\
        .pipe(lambda x: x.drop('created', 1))\
        .pipe(lambda x: x.drop('userId', 1))\
        .pipe(lambda x: x.drop('isActive', 1))\
        .pipe(lambda x: x.drop('userRoleGroup', 1))\
        .pipe(lambda x: x.drop('organisation.id', 1))\
        .pipe(lambda x: x.drop('createdBy', 1))

    normalized = pd.merge(
        urg,
        org,
        how="inner",
        on=None,
        left_on="user.id",
        right_on="userLogin",
        left_index=False,
        right_index=False,
        sort=True,
        suffixes=("_x", "_y"),
        copy=True,
        indicator=False,
        validate=None,
    )\
        .sort_values(["isAusTrakkaAdmin"], ascending=False) \
        .pipe(lambda x: x.drop('userLogin', 1))

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
    email: str,
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
        path=f'{USER_PATH}/{email}',
        body=user
    )
