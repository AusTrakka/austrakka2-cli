from io import BufferedReader

from loguru import logger

from austrakka.utils.fs import verify_hash_single, FileHash
from austrakka.utils.fs import verify_hash_dataset_job
from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_post_multipart, api_post_multipart_raw, get_response
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


@logger_wraps()
def upload_multipart(
        path: str,
        files,
        file_hash: FileHash,
        custom_headers: dict):

    resp = api_post_multipart_raw(
        path=path,
        files=files,
        custom_headers=custom_headers,
    )
    data = get_response(resp, True)
    if resp.status_code == 200:
        verify_hash_single(file_hash, data)


@logger_wraps()
def upload_multipart_tracking_token(
        path: str,
        files,
        file_hash: FileHash,
        custom_headers: dict):

    resp = api_post_multipart_raw(
        path=path,
        files=files,
        custom_headers=custom_headers,
    )
    data = get_response(resp, True)
    dto = data['data']
    logger.info('Checking Hash...')
    verify_hash_dataset_job(file_hash, dto)
    logger.success('Hash Verified!')
    return dto['trackingToken']
