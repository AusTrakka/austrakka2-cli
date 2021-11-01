from io import BufferedReader

from austrakka.utils import logger_wraps
from austrakka.api import call_api
from austrakka.api import post
from austrakka.job.instance.job_instance import add_job_instance


@logger_wraps()
def upload_file(
        file: BufferedReader,
        analysis_id: int,
        species_id: int,
        route: str
):
    job_instance_resp = add_job_instance(
        analysis_id=analysis_id,
        species_id=species_id,
    )

    return call_api(
        method=post,
        path=route,
        body={
            'file': (file.name, file),
            'jobinstanceid': str(job_instance_resp['jobInstanceId']),
        },
        multipart=True,
    )
