from typing import List

import pandas as pd
from loguru import logger

from austrakka.utils.api import call_api
from austrakka.utils.api import get, post, put, patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.paths import GROUP_PATH


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

    call_api(
        method=put,
        path=f'{GROUP_PATH}/{name}',
        body=payload)

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

    return call_api(
        method=post,
        path=GROUP_PATH,
        body=payload)


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

    return call_api(
        method=patch,
        path=f'{GROUP_PATH}/{sub_path}',
        body=payload)


@logger_wraps()
def list_group(out_format: str):
    response = call_api(
        method=get,
        path=GROUP_PATH,
    )

    data = response['data'] if ('data' in response) else response
    result = pd.json_normalize(data, max_level=1)

    if 'organisation' in result.columns:
        result.drop(['organisation'],
                    axis='columns',
                    inplace=True)

    result.fillna('', inplace=True)

    print_table(
        result,
        out_format,
    )
