import os
from pathlib import Path
from io import BufferedReader, StringIO, BytesIO, TextIOWrapper
import codecs
import hashlib
from dataclasses import dataclass
from typing import List, Dict

import httpx
import pandas as pd
# pylint: disable=no-name-in-module
from pandas._libs.parsers import STR_NA_VALUES
from pandas.core.frame import DataFrame
from loguru import logger
from httpx import HTTPStatusError
from Bio import SeqIO

from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.exceptions import UnknownResponseException
from austrakka.utils.exceptions import IncorrectHashException
from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import api_post_multipart_raw
from austrakka.utils.api import api_get
from austrakka.utils.api import get_response
from austrakka.utils.api import api_get_stream
from austrakka.utils.api import set_mode_header
from austrakka.utils.enums.api import RESPONSE_TYPE_ERROR
from austrakka.utils.paths import SEQUENCE_PATH
from austrakka.utils.paths import SEQUENCE_BY_GROUP_PATH
from austrakka.utils.paths import SEQUENCE_BY_SAMPLE_PATH
from austrakka.utils.output import create_response_object
from austrakka.utils.output import log_response
from austrakka.utils.output import log_response_compact
from austrakka.utils.fs import create_dir
from austrakka.utils.enums.seq import FASTA_UPLOAD_TYPE
from austrakka.utils.enums.seq import FASTQ_UPLOAD_TYPE
from austrakka.utils.enums.seq import READ_BOTH
from austrakka.utils.output import print_dataframe
from austrakka.utils.retry import retry
from austrakka.utils.api import api_delete
from austrakka.utils.fs import FileHash, verify_hash

FASTA_PATH = 'Fasta'
FASTQ_PATH = 'Fastq'
DOWNLOAD = 'download'

FASTQ_CSV_SAMPLE_ID = 'Seq_ID'
FASTQ_CSV_SAMPLE_ID_API = 'sample-id'
FASTQ_CSV_PATH_1 = 'filepath1'
FASTQ_CSV_PATH_2 = 'filepath2'
FASTQ_CSV_PATH_1_API = 'filename1'
FASTQ_CSV_PATH_2_API = 'filename2'

FASTA_CSV_SAMPLE = 'SampleId'
FASTA_CSV_FILENAME = 'FileName'
FASTA_CSV_FASTA_ID = 'FastaId'

USE_IS_ACTIVE_FLAG = 'useIsActiveFlag'


@dataclass
class SeqFile:
    multipart: tuple
    sha256: str
    filename: str

@logger_wraps()
def add_fasta_submission(
        fasta_file: BufferedReader,
        skip: bool = False,
        force: bool = False):

    name_prefix = _calc_name_prefix(fasta_file)

    failed_samples = []
    upload_success_count = 0
    total_upload_count = 0
    for record in SeqIO.parse(TextIOWrapper(fasta_file), 'fasta'):
        seq_id = record.id
        logger.info(f"Uploading {seq_id}")
        total_upload_count += 1

        files, file_hash = _fasta_payload(
            name_prefix,
            seq_id,
            record)

        custom_headers = {}
        set_mode_header(custom_headers, force, skip)

        try:
            retry(
                func=lambda f=files, fh=file_hash, ch=custom_headers: _post_fasta(f, fh, ch),
                retries=1,
                desc=f"{seq_id} at " + "/".join([SEQUENCE_PATH, FASTA_PATH]),
                delay=0.0
            )
            upload_success_count += 1
        except FailedResponseException as ex:
            logger.error(f'Sample {seq_id} failed upload')
            log_response(ex.parsed_resp)
            failed_samples.append(seq_id)
        except (
                PermissionError, UnknownResponseException, HTTPStatusError
        ) as ex:
            logger.error(f'Sample {seq_id} failed upload')
            logger.error(ex)
            failed_samples.append(seq_id)

    logger.success(f"Uploaded {upload_success_count} of {total_upload_count} samples")
    if failed_samples:
        failed_samples_str = ", ".join(failed_samples)
        logger.error(f"Failed to upload {len(failed_samples)} samples: {failed_samples_str}")


def _calc_name_prefix(fasta_file):
    original_filename = Path(fasta_file.name)
    if not original_filename:
        original_filename = Path("unnamed.fasta")
    if original_filename.suffix not in [".fa", ".fasta"]:
        raise ValueError("FASTA file suffix is expected to be .fa or .fasta")
    name_prefix = original_filename.stem
    return name_prefix


def _fasta_hash(single_contig, single_contig_filename):
    content = single_contig.getvalue()
    return FileHash(
        filename=single_contig_filename,
        sha256=hashlib.sha256(bytearray(content, 'utf-8')).hexdigest())


def _fasta_payload(name_prefix, seq_id, record):
    """
    Generate the upload files for a single FASTA record:
    Create the single-contig CSV file and FASTA file, and calculate the sequence file hash
    """
    csv, csv_filename, single_contig_filename = _gen_csv(
        name_prefix,
        seq_id)
    single_contig = StringIO()
    SeqIO.write([record], single_contig, "fasta")
    encode = codecs.getwriter('utf-8')
    files = [
        ('files[]', (csv_filename, csv)),
        ('files[]', (single_contig_filename, encode(single_contig)))
    ]
    file_hash = _fasta_hash(
        single_contig,
        single_contig_filename)
    return files, file_hash


def _gen_csv(name_prefix, seq_id):
    csv_filename = f"{name_prefix}_{seq_id}_split.csv"
    single_contig_filename = f"{name_prefix}_{seq_id}_split.fasta"
    csv = BytesIO(
        f"SampleId,FileName,FastaId\n{seq_id},{single_contig_filename},\n".encode())
    return csv, csv_filename, single_contig_filename


def _get_and_validate_csv(csv: BufferedReader, usecols: List[str]):
    try:
        csv_dataframe = pd.read_csv(
            csv,
            usecols=usecols,
            dtype=str
        )
        return csv_dataframe
    except ValueError:
        logger.error(
            "The CSV file mapping samples to sequences must contain exactly "
            f"the column headers {','.join(usecols)}")
        raise


def _fastq_file_2_is_present(row: pd.Series) -> bool:
    return str(row[FASTQ_CSV_PATH_2]) not in STR_NA_VALUES


def _get_file(filepath: str) -> SeqFile:
    # pylint: disable=consider-using-with
    file = open(filepath, 'rb')
    filename = os.path.basename(file.name)
    return SeqFile(
        multipart=('files[]', (filename, file)),
        sha256=hashlib.sha256(file.read()).hexdigest(),
        filename=filename,
    )


def _post_fastq(sample_files: list[SeqFile], custom_headers):
    files = [file.multipart for file in sample_files]
    resp = api_post_multipart_raw(
        path="/".join([SEQUENCE_PATH, FASTQ_PATH]),
        files=files,
        custom_headers=custom_headers,
    )

    data = get_response(resp, True)

    if resp.status_code == 200:
        hashes = [FileHash(filename=f.filename, sha256=f.sha256)
                  for f in sample_files]
        verify_hash(hashes, data)


def _post_fasta(sample_files, file_hash: FileHash, custom_headers: dict):
    resp = api_post_multipart_raw(
        path="/".join([SEQUENCE_PATH, FASTA_PATH]),
        files=sample_files,
        custom_headers=custom_headers,
    )

    data = get_response(resp, True)
    if resp.status_code == 200:
        verify_hash(list([file_hash]), data)


@logger_wraps()
def add_fastq_submission(
        csv: BufferedReader,
        skip: bool = False,
        force: bool = False):
    usecols = [
        FASTQ_CSV_SAMPLE_ID,
        FASTQ_CSV_PATH_1,
        FASTQ_CSV_PATH_2
    ]
    csv_dataframe = _get_and_validate_csv(csv, usecols)

    messages = _validate_fastq_submission(csv_dataframe)
    if messages:
        raise FailedResponseException(messages)

    failed_samples = []
    upload_success_count = 0
    total_upload_count = 0 
    for _, row in csv_dataframe.iterrows():
        try:
            total_upload_count += 1
            
            sample_files = []
            custom_headers = {
                FASTQ_CSV_SAMPLE_ID_API: row[FASTQ_CSV_SAMPLE_ID],
                FASTQ_CSV_PATH_1_API: os.path.basename(row[FASTQ_CSV_PATH_1]),
            }
            sample_files.append(_get_file(row[FASTQ_CSV_PATH_1]))

            if _fastq_file_2_is_present(row):
                custom_headers[FASTQ_CSV_PATH_2_API] \
                    = os.path.basename(row[FASTQ_CSV_PATH_2])
                sample_files.append(_get_file(row[FASTQ_CSV_PATH_2]))

            set_mode_header(custom_headers, force, skip)

            retry(lambda sf=sample_files, ch=custom_headers: _post_fastq(
                sf, ch), 1, "/".join([SEQUENCE_PATH, FASTQ_PATH]))
            upload_success_count += 1
            
        except FailedResponseException as ex:
            logger.error(f'Sample {row[FASTQ_CSV_SAMPLE_ID]} failed upload')
            log_response(ex.parsed_resp)
            failed_samples.append(row[FASTQ_CSV_SAMPLE_ID])
            
        except (
                PermissionError,
                UnknownResponseException,
                HTTPStatusError,
                IncorrectHashException,
        ) as ex:
            logger.error(f'Sample {row[FASTQ_CSV_SAMPLE_ID]} failed upload')
            logger.error(ex)
            failed_samples.append(row[FASTQ_CSV_SAMPLE_ID])
        except Exception as ex:
            raise ex from ex

    logger.info(f"Uploaded {upload_success_count} of {total_upload_count} samples")
    if failed_samples:
        failed_samples_str = ", ".join(failed_samples)
        logger.error(f"Failed to upload {len(failed_samples)} samples: {failed_samples_str}")


def take_sample_names(data, filter_prop):
    try:
        # Expecting response with flat sample summary dtos
        fss_dtos = list(data)
        fastq_fss_dtos = filter(lambda fss: fss[filter_prop], fss_dtos)
        samples_map = map(lambda x: x['sampleName'], fastq_fss_dtos)
        samples_names = list(samples_map)
        return samples_names

    except Exception as ex:
        logger.error(
            'Error while fetching sample names for samples '
            'with fastq files attached: ')
        raise ex from ex


def _validate_fastq_submission(csv_dataframe: DataFrame):
    messages = []

    if csv_dataframe[FASTQ_CSV_PATH_1].isnull().values.any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_PATH_1} column contains missing values',
            RESPONSE_TYPE_ERROR
        ))

    if csv_dataframe[FASTQ_CSV_SAMPLE_ID].isnull().values.any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_SAMPLE_ID} column contains missing values',
            RESPONSE_TYPE_ERROR
        ))
    if csv_dataframe[FASTQ_CSV_SAMPLE_ID].dropna().duplicated().any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_SAMPLE_ID} column contains duplicate values',
            RESPONSE_TYPE_ERROR
        ))
    if csv_dataframe[FASTQ_CSV_PATH_1].dropna().duplicated().any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_PATH_1} column contains duplicate values',
            RESPONSE_TYPE_ERROR
        ))
    if csv_dataframe[FASTQ_CSV_PATH_2].dropna().duplicated().any():
        messages.append(create_response_object(
            f'{FASTQ_CSV_PATH_2} column contains duplicate values',
            RESPONSE_TYPE_ERROR
        ))

    for _, row in csv_dataframe.iterrows():
        if not os.path.isfile(row[FASTQ_CSV_PATH_1]):
            messages.append(create_response_object(
                f'File {row[FASTQ_CSV_PATH_1]} not found',
                RESPONSE_TYPE_ERROR
            ))

        if _fastq_file_2_is_present(row) \
                and not os.path.isfile(row[FASTQ_CSV_PATH_2]):
            messages.append(create_response_object(
                f'File {row[FASTQ_CSV_PATH_2]} not found',
                RESPONSE_TYPE_ERROR
            ))

    return messages


def _download_seq_file(file_path, filename, query_path, sample_dir):
    try:
        def _write_chunks(resp: httpx.Response):
            for chunk in resp.iter_raw(chunk_size=128):
                file.write(chunk)

        if not os.path.exists(sample_dir):
            create_dir(sample_dir)
        with open(file_path, 'wb') as file:
            api_get_stream(query_path, _write_chunks)

        logger.success(f'Downloaded: {filename} To: {file_path}')

    except FailedResponseException as ex:
        log_response_compact(ex.parsed_resp)
    except UnknownResponseException as ex:
        log_response_compact(ex)
    except HTTPStatusError as ex:
        logger.error(
            f'Failed downloading {filename} To: {file_path}. Error: {ex}'
        )
        os.remove(file_path)


def _get_seq_download_path(
        sample_name: str,
        read: str,
        seq_type: str,):

    download_path = f'{SEQUENCE_PATH}/{DOWNLOAD}'
    download_path += f'/{FASTQ_PATH}/{sample_name}/{read}' \
        if seq_type == FASTQ_UPLOAD_TYPE \
        else f'/{FASTA_PATH}/{sample_name}'
    return download_path


def _download_sequences(
        output_dir: str,
        samples_seq_info: list[Dict],
):
    for ssi in samples_seq_info:
        sample_name = ssi['sampleName']
        dto_read = str(ssi['read'])
        filename = ssi['fileNameOnDisk']
        seq_type = ssi['type']

        sample_dir = os.path.join(output_dir, sample_name)
        file_path = os.path.join(sample_dir, filename)

        if os.path.exists(file_path):
            logger.warning(
                f'Found a local copy of {filename}.  Skipping...')
            continue

        query_path = _get_seq_download_path(
            sample_name,
            dto_read,
            seq_type,)

        _download_seq_file(file_path, filename, query_path, sample_dir)


def _filter_sequences(data, seq_type, read) -> List[Dict]:
    data_filtered = list(filter(lambda x: x['type'] == seq_type or seq_type is None, data))
    data_filtered = list(filter(lambda x: x['isActive'] is True, data_filtered))
    if seq_type == FASTA_UPLOAD_TYPE:
        return data_filtered
    data_filtered = list(filter(lambda x: read == READ_BOTH or
                                          x['read'] == int(read), data_filtered))
    return data_filtered


def _get_seq_api(group_name: str):
    api_path = SEQUENCE_PATH
    if group_name is not None:
        api_path += f'/{SEQUENCE_BY_GROUP_PATH}/{group_name}'
    else:
        raise ValueError("A filter has not been passed")
    return api_path


def _get_seq_api_sample_names(sample_ids: List[str]):
    api_path = SEQUENCE_PATH
    paths = []
    if sample_ids is not None:
        for sample in sample_ids:
            api_path += f'/{SEQUENCE_BY_SAMPLE_PATH}/{sample}'
            paths.append(api_path)
            api_path = SEQUENCE_PATH
    else:
        raise ValueError("A filter has not been passed")
    return paths


# pylint: disable=duplicate-code,no-else-return
def _get_seq_data(
        seq_type: str,
        read: str,
        group_name: str,
        sample_ids: List[str] = None,
):
    data = []
    if group_name:
        api_path = _get_seq_api(group_name)
        data = api_get(path=api_path)['data']
        return _filter_sequences(data, seq_type, read)
    else:
        api_paths = _get_seq_api_sample_names(sample_ids)
        for path in api_paths:
            data.extend(api_get(path=path)['data'])
        result = _filter_sequences(data, seq_type, read)
        skipped_samples = [sample for sample in sample_ids if 
                           sample not in [item['sampleName'] for item in result]]
        if skipped_samples:
            logger.warning('Skipped samples with no available sequences: '
                           f'{",".join(skipped_samples)}')
        return result


# pylint: disable=duplicate-code
def get_sequences(
        output_dir,
        seq_type: str,
        read: str,
        group_name: str = None,
        sample_ids: List[str] = None,
):
    if not os.path.exists(output_dir):
        create_dir(output_dir)

    data = _get_seq_data(
        seq_type,
        read,
        group_name,
        sample_ids,
    )
    _download_sequences(output_dir, data)


# pylint: disable=duplicate-code
def list_sequences(
        out_format: str,
        seq_type: str,
        read: str,
        group_name: str,
):
    data = _get_seq_data(
        seq_type,
        read,
        group_name,
    )
    print_dataframe(
        pd.DataFrame(data),
        out_format,
    )


@logger_wraps()
def purge_sequence(sample_id: str, skip: bool, force: bool, delete_all: bool):
    custom_headers = {}
    set_mode_header(custom_headers, force, skip)
    api_path = "/".join([SEQUENCE_PATH, SEQUENCE_BY_SAMPLE_PATH, sample_id])

    if delete_all:
        api_path = api_path + '?deleteAll=true'

    api_delete(
        path=api_path,
        custom_headers=custom_headers
    )
