from io import BufferedReader
from typing import Tuple
from os import path
from collections import Counter

import pandas as pd
# pylint: disable=no-name-in-module
from pandas._libs.parsers import STR_NA_VALUES
from pandas.core.frame import DataFrame
from loguru import logger

from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import post
from austrakka.utils.api import RESPONSE_TYPE_ERROR
from austrakka.utils.paths import SEQUENCE_PATH
from austrakka.utils.output import create_response_object
from austrakka.utils.output import log_response

FASTA_UPLOAD = 'Fasta'
FASTQ_UPLOAD = 'Fastq'

FASTQ_CSV_SAMPLE_ID = 'sampleId'
FASTQ_CSV_FILENAME_1 = 'filename1'
FASTQ_CSV_FILENAME_2 = 'filename2'
FASTQ_CSV_OWNER_ORG = 'ownerOrg'
FASTQ_CSV_SPECIES = 'species'


@logger_wraps()
def add_fasta_submission(files: Tuple[BufferedReader], csv: BufferedReader):
    call_api(
        method=post,
        path=path.join(SEQUENCE_PATH, FASTA_UPLOAD),
        body=[('files[]', (file.name, file)) for file in files]
        + [('files[]', (csv.name, csv))],
        multipart=True,
    )


@logger_wraps()
def add_fastq_submission(files: Tuple[BufferedReader], csv: BufferedReader):
    csv_dataframe = pd.read_csv(
        csv,
        usecols=[
            FASTQ_CSV_SAMPLE_ID,
            FASTQ_CSV_FILENAME_1,
            FASTQ_CSV_FILENAME_2,
            FASTQ_CSV_OWNER_ORG,
            FASTQ_CSV_SPECIES,
        ]
    )

    messages = _validate_fastq_submission(files, csv_dataframe)
    if messages:
        raise FailedResponseException(messages)

    for _, row in csv_dataframe.iterrows():
        custom_headers = {
            FASTQ_CSV_SAMPLE_ID: row[FASTQ_CSV_SAMPLE_ID],
            FASTQ_CSV_FILENAME_1: row[FASTQ_CSV_FILENAME_1],
        }

        if str(row[FASTQ_CSV_FILENAME_2]) not in STR_NA_VALUES:
            custom_headers[FASTQ_CSV_FILENAME_2] = row[FASTQ_CSV_FILENAME_2]

        if str(row[FASTQ_CSV_OWNER_ORG]) not in STR_NA_VALUES:
            custom_headers[FASTQ_CSV_OWNER_ORG] = row[FASTQ_CSV_OWNER_ORG]

        if str(row[FASTQ_CSV_SPECIES]) not in STR_NA_VALUES:
            custom_headers[FASTQ_CSV_SPECIES] = row[FASTQ_CSV_SPECIES]

        sample_files = [
            ('files[]', (file.name, file))
            for file
            in files
            if file.name in [
                row[FASTQ_CSV_FILENAME_1],
                row[FASTQ_CSV_FILENAME_2],
            ]
        ]
        try:
            call_api(
                method=post,
                path=path.join(SEQUENCE_PATH, FASTQ_UPLOAD),
                body=sample_files,
                multipart=True,
                custom_headers=custom_headers,
            )
        except FailedResponseException as ex:
            logger.error(f'Sample {row[FASTQ_CSV_SAMPLE_ID]} failed upload')
            log_response(ex.parsed_resp)
        except Exception as ex:
            raise ex from ex


def _validate_fastq_submission(
        files: Tuple[BufferedReader],
        csv_dataframe: DataFrame,
):
    filenames = [file.name for file in files]

    duplicate_filenames = [
        item for item, count
        in Counter(filenames).items()
        if count > 1
    ]

    messages = []

    if duplicate_filenames:
        # This should probably build a response object, and then throw to let
        # the main exception handler catch and log it correctly.
        for filename in duplicate_filenames:
            messages.append(create_response_object(
                f'Filename {filename} appears twice in passed files',
                RESPONSE_TYPE_ERROR
            ))

    if csv_dataframe[FASTQ_CSV_FILENAME_1].isnull().values.any():
        messages.append(create_response_object(
            'Filename1 column contains missing values',
            RESPONSE_TYPE_ERROR
        ))

    if csv_dataframe[FASTQ_CSV_SAMPLE_ID].isnull().values.any():
        messages.append(create_response_object(
            'SampleId column contains missing values',
            RESPONSE_TYPE_ERROR
        ))
    if csv_dataframe[FASTQ_CSV_SAMPLE_ID].dropna().duplicated().any():
        messages.append(create_response_object(
            'SampleId column contains duplicate values',
            RESPONSE_TYPE_ERROR
        ))
    if csv_dataframe[FASTQ_CSV_FILENAME_1].dropna().duplicated().any():
        messages.append(create_response_object(
            'Filename1 column contains duplicate values',
            RESPONSE_TYPE_ERROR
        ))
    if csv_dataframe[FASTQ_CSV_FILENAME_2].dropna().duplicated().any():
        messages.append(create_response_object(
            'Filename2 column contains duplicate values',
            RESPONSE_TYPE_ERROR
        ))

    for _, row in csv_dataframe.iterrows():
        if row[FASTQ_CSV_FILENAME_1] not in filenames:
            messages.append(create_response_object(
                f'File {row[FASTQ_CSV_FILENAME_1]} not found',
                RESPONSE_TYPE_ERROR
            ))

        if str(row[FASTQ_CSV_FILENAME_2]) not in STR_NA_VALUES \
                and row[FASTQ_CSV_FILENAME_2] not in filenames:
            messages.append(create_response_object(
                f'File {row[FASTQ_CSV_FILENAME_2]} not found',
                RESPONSE_TYPE_ERROR
            ))

    return messages
