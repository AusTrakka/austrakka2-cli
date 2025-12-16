
import os
import pandas as pd
from austrakka.utils.http import HEADERS, get_header_value
import httpx
from httpx import HTTPStatusError
from loguru import logger

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_get, api_post, api_get_stream, api_delete
from austrakka.utils.exceptions import FailedResponseException, UnknownResponseException
from austrakka.utils.fs import FileHash, create_dir, get_hash
from austrakka.utils.retry import retry
from austrakka.utils.helpers.upload import upload_multipart
from austrakka.utils.output import log_response_compact, print_dataframe, log_response, print_response
from austrakka.utils.paths import PROJECT_V2_PATH

DOCUMENT_PATH = 'documents'

@logger_wraps()
def add_document(
        filepath: str,
        description: str,
        abbrev: str):

    path = f'{PROJECT_V2_PATH}/{abbrev}/{DOCUMENT_PATH}'
    file_hash = get_hash(filepath)

    # TODO: Temporary basic sanitisation of description to prevent illegal header value
    safe_description = description.strip()

    with open(filepath, 'rb') as file_content:
        files = [('files[]', (filepath, file_content))]

        custom_headers = {
            'description' : safe_description,
            'filename': os.path.basename(filepath),
        }
        try:
            retry(
                func=lambda f=files, fh=file_hash, ch=custom_headers: _post_document(f, fh, ch, path),
                retries=0,
                desc=f"{abbrev} at " + "/".join([PROJECT_V2_PATH]),
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
        out_format: str):
    
    path = f'{PROJECT_V2_PATH}/{abbrev}/{DOCUMENT_PATH}'
    response = api_get(path)
    data = response['data'] if ('data' in response) else response

    if not data:
        logger.info("No documents available.")
        return
    
    result = pd.DataFrame.from_dict(data)
    print_dataframe(
        result,
        out_format
    )

@logger_wraps()
def download_document(
        abbrev: str,
        document_id: str,
        output_dir: str):
    
    _download_document(abbrev, document_id, output_dir)

@logger_wraps()
def delete_document(
    abbrev: str,
    document_id: str):

    path = f'{PROJECT_V2_PATH}/{abbrev}/{DOCUMENT_PATH}/{document_id}/delete'
    api_delete(path)
    

def _post_document(files, file_hash: FileHash, custom_headers: dict, path):
    upload_multipart(path=path,
                     files=files,
                     file_hash=file_hash,
                     custom_headers=custom_headers)
    

def _download_document(abbrev, document_id, output_dir):
    path = f'{PROJECT_V2_PATH}/{abbrev}/{DOCUMENT_PATH}/{document_id}/download'
    try:
        def _write_chunks(resp: httpx.Response):
            filename = get_header_value(resp, HEADERS.CONTENT_DISPOSITION, "filename")
            file_path = os.path.join(output_dir, filename)

            if os.path.exists(file_path):
                raise FileExistsError(
                    f"File with the same filename already found: {file_path}"
                )

            with open(file_path, "wb") as file:
                for chunk in resp.iter_raw(chunk_size=128):
                    file.write(chunk)

            logger.success(f"Downloaded: {filename} To: {file_path}")
        
        api_get_stream(path, _write_chunks)

    # TODO: Add logging errors here and possibly os.remove() (line in _download_seq_file austrakka/components/sequence/funcs.py)
    except FailedResponseException as ex:
        log_response_compact(ex.parsed_resp)
        logger.error()
    except UnknownResponseException as ex:
        log_response_compact(ex)
        logger.error()
    except HTTPStatusError as ex:
        logger.error(
            f"Failed downloading document with ID {document_id} from {abbrev}. Error: {ex}"
        )

