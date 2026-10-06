# pylint: disable=consider-using-with
from typing import Union
from urllib.parse import urljoin

import httpx
from loguru import logger

def get_server_info(
        url: str, 
        vertify_vert: bool,
) -> Union[tuple[str, str, str], None]:
    data = {}
    try:
        r = httpx.get(urljoin(url, "/api/Version"), verify=not vertify_vert)
        if not r.is_success:
            logger.warning(
                "Unable to contact server to determine auth information.")
            return None
        data = r.json()
    except httpx.HTTPError as ex:
        logger.warning(
            f"Unable to contact server to determine auth information. - {ex}")
        return None
    client_id = data["data"]["clientId"]
    tenant_id = data["data"]["tenantId"]
    api_scope = data["data"]["apiScope"]

    if (client_id == "" or tenant_id == "" or api_scope == ""):
        # Can be removed once AusTrakka is using our single container build
        logger.debug(
            "ServerInfo is incomplete for environment. Using default values."
        )
        return None
    return (client_id, tenant_id, api_scope)
