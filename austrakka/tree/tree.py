from io import BufferedReader

from austrakka.utils import logger_wraps
from austrakka.api import call_api
from austrakka.api import post
from austrakka.job.instance.job_instance import add_job_instance

TREE_ROUTE = 'Tree'
TREE_UPLOAD = 'UploadTree'


@logger_wraps()
def add_tree(file: BufferedReader, analysis_id: int, species_id: int):
    job_instance_resp = add_job_instance(
        analysis_id=analysis_id,
        species_id=species_id,
    )

    call_api(
        method=post,
        path=f'{TREE_ROUTE}/{TREE_UPLOAD}',
        body={
            'file': (file.name, file),
            'jobinstanceid': str(job_instance_resp['jobInstanceId']),
        },
        multipart=True,
    )