from typing import List, Dict, Any

from loguru import logger

from austrakka.utils.api import api_patch, api_get
from austrakka.utils.api import api_post
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import GROUP_PATH, USER_PATH


@logger_wraps()
def list_users(show_disabled: bool, out_format: str):
    call_get_and_print(
        f'{USER_PATH}/?includeall={show_disabled}',
        out_format=out_format,
        datetime_cols=['created','lastUpdated','lastLogIn','lastActive'],
    )


# pylint: disable=duplicate-code
@logger_wraps()
def add_user(
        user_id: str,
        username: str,
        org: str,
        email: str,
        position: str,
        owner_group_roles: List[str],
        is_process: bool,
        server_username: str,
        no_download_quota: bool,
        download_quota: int,
):
    if no_download_quota and download_quota is not None:
        logger.info(f"User configured with no download quota: "
                    f"Quota of {download_quota} will be ignored")
        
    user = {
        "objectId": user_id,
        "username": username,
        "organisation": org,
        "contactEmail": email,
        "position": position,
        "isAusTrakkaProcess": is_process,
        "analysisServerUsername": server_username,
        "monthlyBytesQuota": download_quota,
        "noDownloadQuota": no_download_quota,
    }
    
    api_post(
        path=USER_PATH,
        data=user
    )

    api_patch(
        path=f'{GROUP_PATH}/assign',
        data={
            "identifier": username,
            "entitlements": [
                { "groupName": f"{org}-Owner", "roleName": role} 
                for role 
                in owner_group_roles
            ],
        },
    )


def update_user(
        global_id: str,
        name: str = None,
        email: str = None,
        position: str = None,
        server_username: str = None,
        is_active: bool = None,
        no_download_quota: bool = None,
        download_quota: int = None,
):
    user_resp = api_get(f'{USER_PATH}/{global_id}')
    user_full = user_resp['data']
    user: Dict[str, Any] = {
        "displayName": user_full['displayName'],
        "contactEmail": user_full['contactEmail'],
        "position": user_full['position'],
        "isActive": user_full['isActive'],
        "analysisServerUsername": user_full['analysisServerUsername'],
        "noDownloadQuota": user_full['noDownloadQuota'],
        "monthlyBytesQuota": user_full['monthlyBytesQuota'],
    }

    if no_download_quota and download_quota is not None:
        logger.info(f"User configured with no download quota: "
                    f"Quota of {download_quota} will be ignored")

    if name is not None:
        user['displayName'] = name
    if email is not None:
        user['contactEmail'] = email
    if position is not None:
        user['position'] = position
    if is_active is not None:
        user['isActive'] = is_active
    if server_username is not None:
        user['analysisServerUsername'] = server_username
    if no_download_quota is not None:
        user['noDownloadQuota'] = no_download_quota
    if download_quota is not None:
        user['monthlyBytesQuota'] = download_quota

    api_patch(
        path=f'{USER_PATH}/{global_id}',
        data=user
    )


@logger_wraps()
def enable_user(global_id: str):
    api_patch(path=f'{USER_PATH}/enable/{global_id}')


@logger_wraps()
def disable_user(global_id: str):
    api_patch(path=f'{USER_PATH}/disable/{global_id}')


@logger_wraps()
def rename_user(global_id: str, username: str):
    api_patch(
        path=f'{USER_PATH}/rename/{global_id}',
        data={
            "username": username,
        }
    )
