# pylint: disable=consider-using-with
import json
import os
from pathlib import Path
from typing import Any, Dict, Union

import httpx
from loguru import logger

CONF_ENVIRONMENTS = "Environments"
CONF_SERVER_INFO = "ServerInfo"
CONF_URL = "Url"
CONF_CLIENT_ID = "ClientId"
CONF_TENANT_ID = "TenantId"
CONF_API_SCOPE = "ApiScope"
CONF_USE_SERVER_INFO_ENDPOINT = "UseServerInfoEndpoint"


def get_config_dir() -> str:
    home = Path.home()
    return os.path.join(home, ".config", "trakka")


def get_config_file() -> str:
    return os.path.join(get_config_dir(), "config.json")


def create_config_file_if_not_exists():
    conf_dir = get_config_dir()
    conf_file = get_config_file()
    try:
        if not os.path.isdir(conf_dir):
            logger.debug("Creating config directory at " + conf_dir)
            Path(conf_dir).mkdir(parents=True, exist_ok=True)
        if not os.path.isfile(conf_file):
            with open(conf_file, "a", encoding="utf-8") as f:
                logger.debug("Creating config file at " + conf_file)
                f.write(f"{{\"{CONF_ENVIRONMENTS}\": []}}")
    # pylint: disable=broad-exception-caught
    except Exception as e:
        logger.warning("Unable to create local config.")
        logger.warning(e)



def _get_server_info(url: str, data: Any) -> Union[tuple[str, str, str], None]:
    env_conf = [e for e in data[CONF_ENVIRONMENTS] if e[CONF_URL] == url][0]
    if env_conf is None:
        logger.debug("Config for env " + url + " not found. "
                     + "Using default auth values.")
        return None
    if not env_conf["UseServerInfoEndpoint"]:
        logger.debug("Environment not configured to use server "
                     + "information endpoint. Using default auth values.")
        return None

    client_id = env_conf[CONF_SERVER_INFO][CONF_CLIENT_ID]
    tenant_id = env_conf[CONF_SERVER_INFO][CONF_TENANT_ID]
    api_scope = env_conf[CONF_SERVER_INFO][CONF_API_SCOPE]
    if (client_id == "" or tenant_id == "" or api_scope == ""):
        logger.warning(
            "ServerInfo is incomplete for environment. " +
            "Using default values. If you have issues authenticating, " +
            f"remove the section for {url} from {get_config_file()}"
        )
        return None
    return (
        client_id,
        tenant_id,
        api_scope,
    )


def _server_info_exists(url: str, data: Any) -> bool:
    return not next(
        iter([e for e in data[CONF_ENVIRONMENTS] if e[CONF_URL] == url]), None) is None


def get_server_info_or_create(
        url: str, 
        vertify_vert: bool,
) -> Union[tuple[str, str, str], None]:
    create_config_file_if_not_exists()
    conf_file = get_config_file()
    if not os.path.isfile(conf_file):
        return None
    
    orig_conf = open(conf_file, "r", encoding="utf-8")
    data = json.load(orig_conf)
    orig_conf.close()
    exists = _server_info_exists(url, data)
    if exists:
        return _get_server_info(url, data)
    logger.debug(
        f"Server info does not exist for {url}. Attempting to get it"
    )
    env_entry = _get_new_server_info(url, vertify_vert)
    if env_entry is None:
        return None
    data[CONF_ENVIRONMENTS].append(env_entry)

    upd_conf = open(conf_file, "w", encoding="utf-8")
    json.dump(data, upd_conf, ensure_ascii=False, indent=4)
    upd_conf.close()
    return _get_server_info(url, data)


def _get_new_server_info(url: str, vertify_vert: bool) -> Union[Dict, None]:
    data = {}
    try:
        r = httpx.get(url + "/api/Version", verify=not vertify_vert)
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
    use_server_info_endpoint = (
        client_id != "" and tenant_id != "" and api_scope != "")
    env = {
        CONF_URL: url,
        CONF_USE_SERVER_INFO_ENDPOINT: use_server_info_endpoint,
        CONF_SERVER_INFO: {
            CONF_CLIENT_ID: client_id,
            CONF_TENANT_ID: tenant_id,
            CONF_API_SCOPE: api_scope,
        }
    }
    return env
