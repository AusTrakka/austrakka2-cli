from io import BufferedReader

from ..misc import logger_wraps
from ..api import call_api
from ..api import post
from ...components.job.instance.funcs import add_job_instance


@logger_wraps()
def upload_file(
        file: BufferedReader,
        analysis_abbrev: str,
        route: str
):
    job_instance_resp = add_job_instance(
        analysis_abbrev=analysis_abbrev
    )

    return call_api(
        method=post,
        path=route,
        body={
            'file': (file.name, file),
            'jobinstanceid': str(job_instance_resp['data']['jobInstanceId'])
        },
        multipart=True,
    )
