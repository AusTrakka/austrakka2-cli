
from trakka.utils.api import api_patch
from trakka.utils.misc import logger_wraps
from trakka.utils.paths import USER_PATH

@logger_wraps()
def update_object_id(identifier: str, user_id: str):
    api_patch(
        f"{USER_PATH}/{identifier}/update-object-id/{user_id}",
    )

