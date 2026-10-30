from trakka.utils.api import api_post
from trakka.utils.misc import logger_wraps
from trakka.utils.paths import ANNOUNCEMENT_PATH


@logger_wraps()
def create_announcement(subject: str, body: str, users: list[str]):
    """
    Create an announcement
    """
    data = {
        'Subject': subject,
        'Body': body,
        'Users': users
    }
    api_post(path=ANNOUNCEMENT_PATH, data=data)
