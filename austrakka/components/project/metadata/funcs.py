# pylint: disable=R0801
import json

import httpx
from httpx import HTTPStatusError
from loguru import logger
from austrakka.utils.api import api_get_stream
from austrakka.utils.exceptions import FailedResponseException, UnknownResponseException
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.http import get_header_value, HEADERS
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict
from austrakka.utils.output import log_response_compact
from austrakka.utils.paths import PROJECT_PATH


@logger_wraps()
def get_view(
        abbrev: str,
        out_format: str):
    path = "/".join([PROJECT_PATH, abbrev, 'project-views'])
    call_get_and_print(path, out_format)

@logger_wraps()
def download_view(
        abbrev: str,
        out_format: str
):
    api_path = "/".join([PROJECT_PATH, abbrev, "download-project-view"])
    try:
        def _write_chunks(resp: httpx.Response):
            filename = get_header_value(resp, HEADERS.CONTENT_DISPOSITION, "filename")
            logger.info(f"Downloading file {filename} for {abbrev}")
            json_str = ""
            for chunk in resp.iter_bytes():
                json_str += chunk.decode('utf-8')
            print_dict(json.loads(json_str), out_format)
            logger.success(f"Successfully downloaded file {filename} for {abbrev}")

        api_get_stream(api_path, _write_chunks)

    except FailedResponseException as ex:
        log_response_compact(ex.parsed_resp)
    except UnknownResponseException as ex:
        log_response_compact(ex)
    except HTTPStatusError as ex:
        logger.error(
            f'Failed to download from {abbrev}. Error: {ex}'
        )
