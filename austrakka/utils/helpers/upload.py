from io import BufferedReader

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_post_multipart
from austrakka.utils.api import api_post
from austrakka.utils.paths import JOB_INSTANCE_PATH


@logger_wraps()
def upload_file(
        file: BufferedReader,
        analysis_abbrev: str,
        route: str
):
    job_instance_resp = api_post(
        path=JOB_INSTANCE_PATH,
        data={
            "analysis": {
                "abbreviation": analysis_abbrev,
            }
        }
    )

    return api_post_multipart(
        path=route,
        data={
            'jobinstanceid': str(job_instance_resp['data']['jobInstanceId'])
        },
        files={'file': (file.name, file)}
    )
