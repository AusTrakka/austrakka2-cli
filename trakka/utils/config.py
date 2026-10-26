# pylint: disable=consider-using-with
from urllib.parse import urljoin

import httpx
from loguru import logger

def get_server_info(
        url: str, 
        vertify_vert: bool,
) -> tuple[str, str, str, str]:
    data = {}
    try:
        r = httpx.get(urljoin(url, "/api/Version"), verify=not vertify_vert)
        if not r.is_success:
            raise AuthInfoException(
                "Unable to contact server to determine auth information."
            )
        data = r.json()
    except httpx.HTTPError as ex:
        raise AuthInfoException(
            "Unable to contact server to determine auth information."
        ) from ex
    client_id = data["data"]["clientId"] or ""
    tenant_id = data["data"]["tenantId"] or ""
    api_scope = data["data"]["apiScope"] or ""
    required_cli_version = data["data"]["requiredCliVersion"] or ""

    if (client_id == "" or tenant_id == "" or api_scope == ""):
        raise AuthInfoException(
            "Could not obtain authentication information for server."
        )

    logger.debug("Auth details: ClientId " + client_id + " TenantId "
        + tenant_id + " ApiScope " + api_scope
        + " RequiredCliVersion " + required_cli_version)
    return (client_id, tenant_id, api_scope, required_cli_version)


class AuthInfoException(Exception):
    pass
