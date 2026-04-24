
import os
from loguru import logger
import httpx
from httpx import HTTPStatusError
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.http import HEADERS, get_header_value
from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_patch, api_get_stream
from austrakka.utils.exceptions import FailedResponseException, UnknownResponseException
from austrakka.utils.fs import FileHash, get_hash
from austrakka.utils.retry import retry
from austrakka.utils.helpers.upload import upload_multipart
from austrakka.utils.output import log_response_compact, log_response
from austrakka.utils.paths import PROJECT_PATH

DOCUMENT_PATH = 'documents'

@logger_wraps()
def add_document(
        filepath: str,
        description: str,
        abbrev: str):

    path = f'{PROJECT_PATH}/{abbrev}/{DOCUMENT_PATH}/upload'
    file_hash = get_hash(filepath)

    safe_description = description.strip()

    with open(filepath, 'rb') as file_content:
        files = [('files[]', (filepath, file_content))]

        custom_headers = {
            'X-Metadata-Description' : safe_description,
            'X-Metadata-Filename': os.path.basename(filepath),
        }
        try:
            retry(
                func=lambda f=files,
                fh=file_hash,
                ch=custom_headers: _post_document(f, fh, ch, path),
                retries=0,
                desc=f"{abbrev} at " + "/".join([PROJECT_PATH]),
                delay=0.0
            )
        except FailedResponseException as ex:
            logger.error(f'Document {filepath} failed upload')
            log_response(ex.parsed_resp)
        except (
                PermissionError, UnknownResponseException, HTTPStatusError
        ) as ex:
            logger.error(f'Document {filepath} failed upload')
            logger.error(ex)


@logger_wraps()
def get_document_list(
        abbrev: str,
        out_format: str,
        show_disabled: bool):
    
    path = f'{PROJECT_PATH}/{abbrev}/{DOCUMENT_PATH}'
    params = { "showDisabled": str(show_disabled).lower() }

    call_get_and_print(
        path,
        params=params,
        out_format=out_format,
        datetime_cols=['uploadedDate'],
    )

@logger_wraps()
def download_document(
        abbrev: str,
        document_id: str,
        output_dir: str):
    
    _download_document(abbrev, document_id, output_dir)

@logger_wraps()
def disable_document(
    abbrev: str,
    document_id: str):

    path = f'{PROJECT_PATH}/{abbrev}/{DOCUMENT_PATH}/{document_id}/disable'
    api_patch(path)

@logger_wraps()
def enable_document(
    abbrev: str,
    document_id: str):

    path = f'{PROJECT_PATH}/{abbrev}/{DOCUMENT_PATH}/{document_id}/enable'
    api_patch(path)
    

def _post_document(files, file_hash: FileHash, custom_headers: dict, path):
    upload_multipart(path=path,
                     files=files,
                     file_hash=file_hash,
                     custom_headers=custom_headers)
    

def _download_document(abbrev, document_id, output_dir):
    path = f'{PROJECT_PATH}/{abbrev}/{DOCUMENT_PATH}/{document_id}/download'
    try:
        def _write_chunks(resp: httpx.Response):
            filename = get_header_value(resp, HEADERS.CONTENT_DISPOSITION, "filename")
            file_path = os.path.join(output_dir, filename)
            file_path = _get_unqiue_filepath(file_path)

            with open(file_path, "wb") as file:
                for chunk in resp.iter_raw(chunk_size=128):
                    file.write(chunk)

            logger.success(f"Downloaded: {filename} To: {file_path}")
        
        api_get_stream(path, _write_chunks)

    except FailedResponseException as ex:
        log_response_compact(ex.parsed_resp)
        logger.error(
            f"Failed downloading document with ID {document_id} from {abbrev}. Error: {ex}"
        )
    except UnknownResponseException as ex:
        log_response_compact(ex)
        logger.error(
            f"Failed downloading document with ID {document_id} from {abbrev}. Error: {ex}"
        )
    except HTTPStatusError as ex:
        logger.error(
            f"Failed downloading document with ID {document_id} from {abbrev}. Error: {ex}"
        )

def _get_unqiue_filepath(file_path) -> str:
    if not os.path.exists(file_path):
        return file_path
    
    base, ext = os.path.splitext(file_path)
    counter = 1

    while True:
        new_file_path = f"{base}({counter}){ext}"
        if not os.path.exists(new_file_path):
            return new_file_path
        counter += 1

def update_document(
    abbrev: str,
    document_id: int,
    file_name: str,
    description: str
):
    path = f'{PROJECT_PATH}/{abbrev}/{DOCUMENT_PATH}/{document_id}/update'
    body = {
        'FileName': file_name,
        'Description': description
    }
    api_patch(path, data=body)
