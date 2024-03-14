# pylint: disable=R0801
import os

import httpx
import pandas as pd
from httpx import HTTPStatusError
from loguru import logger
from austrakka.utils.api import api_get, api_get_stream_with_filename, api_patch
from austrakka.utils.exceptions import FailedResponseException, UnknownResponseException
from austrakka.utils.fs import create_dir
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_formatted, log_response_compact
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

    result = pd.DataFrame.from_dict(data)
    print_formatted(
        result,
        out_format,
    )


@logger_wraps()
def download_dataset_view(
        output_dir: str,
        dataset_view_id: str,
        abbrev: str):
    if not os.path.exists(output_dir):
        create_dir(output_dir)

    path = "/".join([PROJECT_PATH, abbrev, 'download-project-view', dataset_view_id])
    _download_dataset_view_file(output_dir, path)


def _download_dataset_view_file(dir_path, query_path):
    try:
        def _write_chunks(resp: httpx.Response, file):
            for chunk in resp.iter_bytes():
                file.write(chunk)
        api_get_stream_with_filename(query_path, _write_chunks, dir_path)

        logger.success(f'Downloaded to: {dir_path}')

    except FailedResponseException as ex:
        log_response_compact(ex.parsed_resp)
    except UnknownResponseException as ex:
        log_response_compact(ex)
    except HTTPStatusError as ex:
        logger.error(
            f'Failed downloading to: {dir_path}. Error: {ex}'
        )
        os.remove(dir_path)
