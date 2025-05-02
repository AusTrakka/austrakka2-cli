from loguru import logger

from austrakka.utils.fs import verify_hash_single, FileHash
from austrakka.utils.fs import verify_hash_dataset_job
from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_post_multipart_raw, get_response


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
