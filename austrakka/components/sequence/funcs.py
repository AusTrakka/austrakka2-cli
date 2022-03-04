from io import BufferedReader
from typing import Tuple

from loguru import logger

from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import post
from austrakka.utils.api import FailedResponseException
from austrakka.utils.api import RESPONSE_TYPE
from austrakka.utils.api import RESPONSE_TYPE_ERROR
from austrakka.utils.api import RESPONSE_TYPE_SUCCESS
from austrakka.utils.api import RESPONSE_MESSAGE
from austrakka.utils.api import RESPONSE_ROW_NUMBER
from austrakka.utils.output import log_dict
from austrakka.utils.paths import SUBMISSION_PATH

SUBMISSION_UPLOAD = 'UploadSequenceFile'


@logger_wraps()
def add_sequence_submission(files: Tuple[BufferedReader]):
    try:
        call_api(
            method=post,
            path=f'{SUBMISSION_PATH}/{SUBMISSION_UPLOAD}',
            body=[('files[]', (file.name, file)) for file in files],
            multipart=True,
        )
    except FailedResponseException as ex:
        for item in ex.parsed_resp:
            if item[RESPONSE_TYPE] == RESPONSE_TYPE_SUCCESS:
                log_dict({item.pop(RESPONSE_TYPE): item}, logger.success)
            elif item[RESPONSE_TYPE] == RESPONSE_TYPE_ERROR:
                log_dict({item.pop(RESPONSE_TYPE): item}, logger.error)
            else:
                logger.warning(
                    f'Unknown {RESPONSE_TYPE}: "{item[RESPONSE_TYPE]}" ' +
                    f'with {RESPONSE_MESSAGE}: "{item[RESPONSE_MESSAGE]}" ' +
                    f'and {RESPONSE_ROW_NUMBER}: "{item[RESPONSE_ROW_NUMBER]}"')
