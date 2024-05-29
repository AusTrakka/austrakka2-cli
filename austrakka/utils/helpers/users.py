from austrakka.utils.api import api_get
from austrakka.utils.paths import USER_PATH


def get_user(user_id: str):
    return api_get(path=f"{USER_PATH}/userId/{user_id}")['data']
