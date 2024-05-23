# pylint: disable=R0801
import json
import os

import httpx
from httpx import HTTPStatusError
from loguru import logger
from austrakka.utils.api import api_get, api_get_stream, api_patch
from austrakka.utils.exceptions import FailedResponseException, UnknownResponseException
from austrakka.utils.fs import create_dir
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict
from austrakka.utils.output import log_response_compact
from austrakka.utils.output import write_dict
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
        output_dir: str,
        dataset_view_id: str,
        abbrev: str,
        out_format: str
):
    if not os.path.exists(output_dir):
        create_dir(output_dir)

    query_path = "/".join([PROJECT_PATH, abbrev, 'download-project-view', dataset_view_id])
    try:
        def _write_chunks(resp: httpx.Response):
            content_disposition = resp.headers.get("Content-Disposition")
            if not content_disposition:
                raise ValueError("Content-Disposition header not found in response")
            filename = content_disposition.split(";")[1].split("=")[1].strip('"')
            json_str = ""
            for chunk in resp.iter_bytes():
                json_str += chunk.decode('utf-8')
            filepath = os.path.join(output_dir, filename.split('.json')[0])
            write_dict(json.loads(json_str), filepath, out_format)

        api_get_stream(query_path, _write_chunks)

        logger.success(f'Downloaded to: {output_dir}')

    except FailedResponseException as ex:
        log_response_compact(ex.parsed_resp)
    except UnknownResponseException as ex:
        log_response_compact(ex)
    except HTTPStatusError as ex:
        logger.error(
            f'Failed downloading to: {output_dir}. Error: {ex}'
        )
        os.remove(output_dir)
