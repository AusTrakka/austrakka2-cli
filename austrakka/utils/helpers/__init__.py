from austrakka.utils.api import api_get


def _get_by_identifier(path: str, identifier: str):
    return api_get(path=f"{path}/{identifier}")['data']
