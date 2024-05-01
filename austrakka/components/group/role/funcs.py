from typing import List

from loguru import logger

from austrakka.utils.api import api_patch
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import GROUP_PATH


@logger_wraps()
def list_role(show_disabled: bool, out_format: str):
    call_get_and_print(f'{GROUP_PATH}/assignments?includeall={show_disabled}', out_format)


@logger_wraps()
def add_role(
        user_id: str,
        group_roles: List[str]):

    sub_path = "assign"
    return change_user_group_assignment(user_id, group_roles, sub_path)


@logger_wraps()
def remove_role(
        user_id: str,
        group_roles: List[str]):

    sub_path = "unassign"
    return change_user_group_assignment(user_id, group_roles, sub_path)


def change_user_group_assignment(user_id, group_roles, sub_path):
    if len(group_roles) == 0:
        logger.warning("Nothing to do.")
        return None

    group_role_pairs = []
    for group_role in group_roles:
        pairs = group_role.split(",")
        group_role_pairs.append({
            "groupName": pairs[0],
            "roleName": pairs[1]
        })

    payload = {
        "objectId": user_id,
        "entitlements": group_role_pairs
    }

    return api_patch(
        path=f'{GROUP_PATH}/{sub_path}',
        data=payload,
    )
