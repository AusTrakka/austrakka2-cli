# pylint: disable=R0801
import os
import time

from loguru import logger
from austrakka.utils.api import api_post, api_get, api_patch
from austrakka.utils.fs import get_hash
from austrakka.utils.helpers.output import call_get_and_print_table_on_state_change
from austrakka.utils.helpers.output import call_get_and_print_dataset_status
from austrakka.utils.helpers.upload import upload_multipart_tracking_token
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dict
from austrakka.utils.paths import PROJECT_PATH

DATASET_UPLOAD_PATH = 'dataset'
DATASET_ACK_PATH = 'acknowledge'
DATASET_TRACK_PATH = 'dataset-progress'
DATASET_TRACK_DETAILED_PATH = 'dataset-progress-details'


@logger_wraps()
def add_dataset(
        filepath: str,
        label: str,
        abbrev: str):

    path = "/".join([PROJECT_PATH, abbrev, DATASET_UPLOAD_PATH])
    filename = os.path.basename(filepath)
    custom_headers = {
        'analysis-label': label,
        'filename': filename,
    }

    file_hash = get_hash(filepath)
    with open(filepath, 'rb') as file_content:
        files = [('files[]', (filename, file_content))]
        tracking_token = upload_multipart_tracking_token(path=path,
                                                         files=files,
                                                         file_hash=file_hash,
                                                         custom_headers=custom_headers)
    logger.info('Acknowledging...')
    path_ack = "/".join([PROJECT_PATH, abbrev, DATASET_ACK_PATH, tracking_token])
    return api_post(
        path=path_ack,
    )


@logger_wraps()
def track_dataset(
        abbrev:str,
        tracking_token: str,
        detailed: bool,
        out_format: str):
    if detailed:
        print_detailed_job_feedbacks(out_format, abbrev, tracking_token)
    else:
        path = "/".join([PROJECT_PATH,
                         abbrev,
                         DATASET_TRACK_PATH,
                         tracking_token])
        call_get_and_print_dataset_status(
            path,
            out_format
        )


@logger_wraps()
def add_dataset_blocking(
        filepath: str,
        label: str,
        abbrev: str,
        out_format: str):
    logger.info('Storing')
    path_adding = "/".join([PROJECT_PATH, abbrev, DATASET_UPLOAD_PATH])
    filename = os.path.basename(filepath)

    custom_headers = {
        'analysis-label': label,
        'filename': filename,
    }

    file_hash = get_hash(filepath)
    with open(filepath, 'rb') as file_content:
        files = [('files[]', (filename, file_content))]
        tracking_token = upload_multipart_tracking_token(path=path_adding,
                                                         files=files,
                                                         file_hash=file_hash,
                                                         custom_headers=custom_headers)
    path_ack = "/".join([PROJECT_PATH, abbrev, DATASET_ACK_PATH, tracking_token])
    api_post(
        path=path_ack,
    )
    path_track = "/".join([PROJECT_PATH,
                           abbrev,
                           DATASET_TRACK_PATH,
                           tracking_token])

    while True:
        logger.info('Tracking...')
        status_change = call_get_and_print_table_on_state_change(
            path_track,
            out_format,
            'Acknowledged',
        )  # Replace this with your actual function to fetch status

        if status_change is not None:
            logger.success(f"Current status: {status_change}")
            if status_change == 'Finished':
                logger.success('')
                break  # Exit the loop when the desired status is reached
            if "Failed" in status_change:
                logger.error("The dataset ingest has failed")
                break
        else:
            logger.warning('No State Change...')
        time.sleep(5)
    logger.warning("Job Logs:")
    print_detailed_job_feedbacks(out_format, abbrev, tracking_token)


@logger_wraps()
def disable_dataset(
        abbrev: str,
        dataset_id: int):
    path = "/".join([PROJECT_PATH, abbrev, 'disable-dataset', dataset_id])
    return api_patch(
        path=path,
    )


@logger_wraps()
def active_dataset_entry_list_get(abbrev: str, out_format: str):
    path = "/".join([PROJECT_PATH, abbrev, 'active-dataset-entry-list'])
    response = api_get(path)
    data = response['data'] if ('data' in response) else response
    if not data:
        logger.info("No Active Datasets available")
        return

    print_dict(
        data,
        out_format,
    )


def print_detailed_job_feedbacks(out_format: str, abbrev: str, tracking_token: str):
    path = "/".join([PROJECT_PATH, abbrev, DATASET_TRACK_DETAILED_PATH, tracking_token])
    response = api_get(path)
    data = response['data'] if ('data' in response) else response
    if not data:
        logger.info("No JobFeedbacks available")
        return
    print_dict(
        data,
        out_format,
    )
