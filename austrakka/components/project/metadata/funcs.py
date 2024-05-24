# pylint: disable=R0801
import json

import httpx
from httpx import HTTPStatusError
from loguru import logger
from austrakka.utils.api import api_get, api_get_stream, api_patch
from austrakka.utils.exceptions import FailedResponseException, UnknownResponseException
from austrakka.utils.http import get_header_value, HEADERS
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict
from austrakka.utils.output import log_response_compact
from austrakka.utils.paths import PROJECT_PATH

DATASET_UPLOAD_PATH = 'dataset'
DATASET_ACK_PATH = 'acknowledge'
DATASET_TRACK_PATH = 'dataset-progress'
DATASET_TRACK_DETAILED_PATH = 'dataset-progress-details'


@logger_wraps()
def set_merge_algorithm_project(abbrev: str, merge_algorithm: str):
    if merge_algorithm == 'show-all':
        merge_algorithm = 'ShowAll'
    else:
        merge_algorithm = 'Override'

    return api_patch(
        path=f'{PROJECT_PATH}/{abbrev}/set-merge-algorithm/{merge_algorithm}'
    )


@logger_wraps()
def list_dataset_views(
        abbrev: str,
        out_format: str):
    path = "/".join([PROJECT_PATH, abbrev, 'project-views'])
    response = api_get(path)
    data = response['data'] if ('data' in response) else response
    if not data:
        logger.info("No Views available")
        return

    print_dict(
        data,
        out_format,
    )


@logger_wraps()
def download_dataset_view(
        dataset_view_id: str,
        abbrev: str,
        out_format: str
):
    query_path = "/".join([PROJECT_PATH, abbrev, 'download-project-view', dataset_view_id])
    try:
        def _write_chunks(resp: httpx.Response):
            filename = get_header_value(resp, HEADERS.CONTENT_DISPOSITION, "filename")
            logger.info(f"Downloading file {filename} for dataset {dataset_view_id} of {abbrev}")
            json_str = ""
            for chunk in resp.iter_bytes():
                json_str += chunk.decode('utf-8')
            print_dict(json.loads(json_str), out_format)
            logger.success(f"Successfully downloaded file {filename} "
                           f"for dataset {dataset_view_id} of {abbrev}")

        api_get_stream(query_path, _write_chunks)

    except FailedResponseException as ex:
        log_response_compact(ex.parsed_resp)
    except UnknownResponseException as ex:
        log_response_compact(ex)
    except HTTPStatusError as ex:
        logger.error(
            f'Failed to download dataset {dataset_view_id} of {abbrev}. Error: {ex}'
        )
