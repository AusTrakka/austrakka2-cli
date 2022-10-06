from typing import List

import pandas as pd

from austrakka.utils.api import call_api
from austrakka.utils.api import get
from austrakka.utils.api import post
from austrakka.utils.api import put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import USER_PATH
from austrakka.utils.helpers.output import call_get_and_print_table


@logger_wraps()
def list_users(out_format: str):
    call_get_and_print_table(USER_PATH, out_format)


@logger_wraps()
def add_user(
    user_id: str,
    org: str,
    owner_group_roles: List[str],
):
    user = {
        "objectId": user_id,
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
