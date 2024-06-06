from typing import List, Dict, Any

from austrakka.utils.api import api_patch, api_get
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import USER_PATH


@logger_wraps()
def list_users(show_disabled: bool, out_format: str):
    call_get_and_print(f'{USER_PATH}/?includeall={show_disabled}', out_format)


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


def update_user(
        object_id: str,
        name: str = None,
        email: str = None,
        org: str = None,
        is_active: bool = None,
):
    user_resp = api_get(f'{USER_PATH}/userId/{object_id}')
    user_full = user_resp['data']
    user: Dict[str, Any] = {
        "displayName": user_full['displayName'],
        "contactEmail": user_full['contactEmail'],
        "orgAbbrev": user_full['orgAbbrev'],
        "isActive": user_full['isActive'],
    }

    if name is not None:
        user['displayName'] = name
    if email is not None:
        user['contactEmail'] = email
    if org is not None:
        user['orgAbbrev'] = org
    if is_active is not None:
        user['isActive'] = is_active

    api_put(
        path=f'{USER_PATH}/{object_id}',
        data=user
    )


@logger_wraps()
def enable_user(user_id: str):
    api_patch(path=f'{USER_PATH}/enable/{user_id}')


@logger_wraps()
def disable_user(user_id: str):
    api_patch(path=f'{USER_PATH}/disable/{user_id}')
