from typing import List

from austrakka.utils.api import api_patch
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import USER_PATH


@logger_wraps()
def list_users(show_disabled: bool, out_format: str):
    call_get_and_print(f'{USER_PATH}/minimal?includeall={show_disabled}', out_format)


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
    user_id: str,
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
