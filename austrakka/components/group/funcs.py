from typing import List

from loguru import logger

from austrakka.utils.api import api_get
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.api import api_patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import GROUP_PATH
from austrakka.utils.helpers.groups import format_group_dto_for_output


@logger_wraps()
def update_group(
        name: str,
        newname: str,
        org: str):

    payload = {}

    if newname:
        payload["name"] = newname

    if org:
        payload["organisation"] = {"abbreviation": org}

    api_put(
        path=f'{GROUP_PATH}/{name}',
        data=payload)

    logger.info('Done.')


@logger_wraps()
def add_group(
        name: str,
        org: str):

    payload = {
        "name": name,
    }

    if org:
        payload["organisation"] = {"abbreviation": org}

    return api_post(
        path=GROUP_PATH,
        data=payload)


@logger_wraps()
def assign_groups(
        user_id: str,
        group_roles: List[str]):

    sub_path = "assign"
    return change_user_group_assignment(user_id, group_roles, sub_path)


@logger_wraps()
def unassign_groups(
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


@logger_wraps()
def list_group(out_format: str):
    response = api_get(
        path=GROUP_PATH,
    )

    data = response['data'] if ('data' in response) else response
    format_group_dto_for_output(data, out_format)
