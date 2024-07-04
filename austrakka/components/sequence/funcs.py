import os
from pathlib import Path
from io import BufferedReader, StringIO, TextIOWrapper, BytesIO
import codecs
import hashlib
from dataclasses import dataclass
from typing import List, Dict

import httpx
import pandas as pd
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
from austrakka.utils.enums.api import RESPONSE_TYPE_ERROR
from austrakka.utils.paths import SEQUENCE_PATH, SEQUENCE_TYPE_QUERY, SEQUENCE_READ_QUERY
from austrakka.utils.paths import SEQUENCE_DOWNLOAD_PATH
from austrakka.utils.paths import SEQUENCE_BY_GROUP_PATH
from austrakka.utils.paths import SEQUENCE_BY_SAMPLE_PATH
from austrakka.utils.output import create_response_object
from austrakka.utils.output import log_response
from austrakka.utils.output import log_response_compact
from austrakka.utils.fs import create_dir

from austrakka.utils.output import print_dataframe
from austrakka.utils.enums.seq import SeqType
from austrakka.utils.retry import retry
from austrakka.utils.api import api_delete
from austrakka.utils.fs import FileHash, verify_hash

SEQ_ID_CSV = 'Seq_ID'
SEQ_ID_HEADER = 'seq-id'
PATH_CSV = 'filepath'
PATH_HEADER = 'filename'
PATH_1_CSV = 'filepath1'
PATH_2_CSV = 'filepath2'
PATH_1_HEADER = 'filename1'
PATH_2_HEADER = 'filename2'

# Map CSV columns into their relevant headers
HEADER_MAP = {
    SEQ_ID_CSV: SEQ_ID_HEADER,
    PATH_1_CSV: PATH_1_HEADER,
    PATH_2_CSV: PATH_2_HEADER,
    PATH_CSV: PATH_HEADER,
}

USE_IS_ACTIVE_FLAG = 'useIsActiveFlag'

MODE_HEADER = 'mode'
MODE_SKIP = 'skip'
MODE_OVERWRITE = 'overwrite'
SEQTYPE_HEADER = 'seq-type'

CSV_COLUMNS = {
    SeqType.FASTQ_ILL_PE: [SEQ_ID_CSV, PATH_1_CSV, PATH_2_CSV],
}

def _csv_columns(seq_type: SeqType):
    if seq_type in CSV_COLUMNS:
        return CSV_COLUMNS[seq_type]
    return [SEQ_ID_CSV, PATH_CSV]


@dataclass
class SeqFile:
    multipart: tuple
    sha256: str
    filename: str

@logger_wraps()
def add_fasta_cns_submission(
        fasta_file: BufferedReader,
        skip: bool = False,
        force: bool = False):
    '''Iterate through a FASTA file and submit each sequence as a separate sample'''

    name_prefix = _calc_name_prefix(fasta_file)

    failed_samples = []
    upload_success_count = 0
    total_upload_count = 0
    for record in SeqIO.parse(TextIOWrapper(fasta_file), 'fasta'):
        seq_id = record.id
        logger.info(f"Uploading {seq_id}")
        total_upload_count += 1

        file = _create_single_contig_file(
            name_prefix,
            seq_id,
            record)

        custom_headers = _build_headers(
            SeqType.FASTA_CNS, 
            pd.Series({SEQ_ID_CSV: seq_id, PATH_CSV: file.filename}),
            force,
            skip,
        )

        try:
            retry(
                func=lambda f=[file], ch=custom_headers: _post_sequence(f, ch),
                retries=1,
                desc=f"{seq_id} at " + SEQUENCE_PATH,
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

def _create_single_contig_file(name_prefix, seq_id, record) -> SeqFile:
    """
    Generate the upload single-contig FASTA file for a single FASTA record
    """
    single_contig_filename = f"{name_prefix}_{seq_id}_split.fasta"
    single_contig = StringIO()
    SeqIO.write([record], single_contig, "fasta")
    encode = codecs.getwriter('utf-8')
    return SeqFile(
        multipart=('files[]', (single_contig_filename, encode(single_contig))),
        sha256=hashlib.sha256(single_contig.getvalue().encode()).hexdigest(),
        filename=single_contig_filename,
    )


def _get_and_validate_csv(csv: BufferedReader, seq_type: SeqType):
    
    usecols = _csv_columns(seq_type)
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


def _post_sequence(sample_files: list[SeqFile], custom_headers):
    '''Post sequence files to the API and verify hashes. seq-type is sent in headers.'''
    files = [file.multipart for file in sample_files]
    resp = api_post_multipart_raw(
        path=SEQUENCE_PATH,
        files=files,
        custom_headers=custom_headers,
    )

    data = get_response(resp, True)

    if resp.status_code == 200:
        hashes = [FileHash(filename=f.filename, sha256=f.sha256)
                  for f in sample_files]
        verify_hash(hashes, data)


@logger_wraps()
def add_sequence_submission(
        seq_type: SeqType,
        csv: BufferedReader,
        skip: bool = False,
        force: bool = False):
    '''
    Generic handling of uploading any sequence type.
    Handles the case where the user provides a CSV mapping Seq_IDs to files.
    '''
    csv_dataframe = _get_and_validate_csv(csv, seq_type)

    messages = _validate_csv_sequence_submission(csv_dataframe, seq_type)
    if messages:
        raise ValueError(messages)

    failed_samples = []
    upload_success_count = 0
    total_upload_count = 0 
    for _, row in csv_dataframe.iterrows():
        try:
            logger.info(f"Uploading {row[SEQ_ID_CSV]}")
            total_upload_count += 1
            
            custom_headers = _build_headers(seq_type, row, force, skip)
            sample_files = _get_files_from_csv_paths(row, seq_type)

            retry(lambda sf=sample_files, ch=custom_headers: _post_sequence(
                sf, ch), 1, "/".join([SEQUENCE_PATH]))
            upload_success_count += 1
            
        except FailedResponseException as ex:
            logger.error(f'Sample {row[SEQ_ID_CSV]} failed upload')
            log_response(ex.parsed_resp)
            failed_samples.append(row[SEQ_ID_CSV])
            
        except (
                PermissionError,
                UnknownResponseException,
                HTTPStatusError,
                IncorrectHashException,
        ) as ex:
            logger.error(f'Sample {row[SEQ_ID_CSV]} failed upload')
            logger.error(ex)
            failed_samples.append(row[SEQ_ID_CSV])
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


def _validate_csv_sequence_submission(csv_dataframe: DataFrame, seq_type: SeqType):
    messages = []
    
    # Check for missing values
    for column in csv_dataframe.columns:
        if csv_dataframe[column].isnull().values.any():
            messages.append(create_response_object(
                f'{column} column contains missing values',
                RESPONSE_TYPE_ERROR
            ))

    # Check for duplicate values
    for column in csv_dataframe.columns:
        if csv_dataframe[column].duplicated().any():
            messages.append(create_response_object(
                f'{column} column contains duplicate values',
                RESPONSE_TYPE_ERROR
            ))
    
    # In the case of paired-end data, check no file pairs are the same
    if seq_type == SeqType.FASTQ_ILL_PE:
        for _,row in csv_dataframe.iterrows():
            if row[PATH_1_CSV] == row[PATH_2_CSV]:
                messages.append(create_response_object(
                    f'Read files for {row[SEQ_ID_CSV]} are the same',
                    RESPONSE_TYPE_ERROR
                ))
    
    # Check files are present
    for _, row in csv_dataframe.iterrows():
        _check_csv_files(row, messages)
    
    return messages


def _download_seq_file(file_path, filename, query_path, params, sample_dir):
    try:
        def _write_chunks(resp: httpx.Response):
            for chunk in resp.iter_raw(chunk_size=128):
                file.write(chunk)

        if not os.path.exists(sample_dir):
            create_dir(sample_dir)
        with open(file_path, 'wb') as file:
            api_get_stream(query_path, _write_chunks, params)

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
        seq_id: str,
        read: str,
        seq_type: str,):
    download_path = f'{SEQUENCE_PATH}/{SEQUENCE_DOWNLOAD_PATH}/{seq_id}'
    params = {
        SEQUENCE_TYPE_QUERY: seq_type,
    }
    if seq_type==SeqType.FASTQ_ILL_PE.value:
        params[SEQUENCE_READ_QUERY] = read

    return download_path, params


def _download_sequences(
        output_dir: str,
        samples_seq_info: pd.DataFrame,
):
    for _i,ssi in samples_seq_info.iterrows():
        sample_name = ssi['sampleName']
        dto_read = str(ssi['read'])
        filename = ssi['fileNameOnDisk']
        seq_type = ssi['type']

        sample_dir = os.path.join(output_dir, sample_name, seq_type)
        file_path = os.path.join(sample_dir, filename)

        if os.path.exists(file_path):
            logger.warning(
                f'Found a local copy of {filename}.  Skipping...')
            continue

        query_path, params = _get_seq_download_path(
            sample_name,
            dto_read,
            seq_type,)

        _download_seq_file(file_path, filename, query_path, params, sample_dir)

def _filter_sequences(data, seq_type: SeqType) -> List[Dict]:
    data_filtered = list(filter(lambda x: x['type'] == seq_type or seq_type is None, data))
    data_filtered = list(filter(lambda x: x['isActive'] is True, data_filtered))
    return data_filtered


def _get_seq_api_by_group(group_name: str):
    api_path = SEQUENCE_PATH
    if group_name is not None:
        api_path += f'/{SEQUENCE_BY_GROUP_PATH}/{group_name}'
    else:
        raise ValueError("A filter has not been passed")
    return api_path


def _get_seq_api_by_sample_names(sample_ids: List[str]):
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
        group_name: str,
        sample_ids: List[str] = None,
):
    if group_name is None and (sample_ids is None or len(sample_ids)==0):
        raise ValueError(
            "Either group name or Seq_IDs must be provided to get sequence information")
    data = []
    if group_name:
        api_path = _get_seq_api_by_group(group_name)
        data = api_get(path=api_path)['data']
        result = _filter_sequences(data, seq_type)
    else:
        api_paths = _get_seq_api_by_sample_names(sample_ids)
        for path in api_paths:
            data.extend(api_get(path=path)['data'])
        result = _filter_sequences(data, seq_type)
        skipped_samples = [sample for sample in sample_ids if 
                           sample not in [item['sampleName'] for item in result]]
        if skipped_samples:
            logger.warning('Skipped samples with no available sequences: '
                           f'{",".join(skipped_samples)}')
    df = pd.DataFrame(result, dtype=str)
    # pd DF from records is coercing read to a float and producing nans regardless of dtype
    df['read'] = pd.Series([row['read'] for row in result], dtype=str)
    return df


# pylint: disable=duplicate-code
def get_sequences(
        output_dir,
        seq_type: str,
        group_name: str = None,
        sample_ids: List[str] = None,
):
    if not os.path.exists(output_dir):
        create_dir(output_dir)

    data = _get_seq_data(
        seq_type,
        group_name,
        sample_ids,
    )
    _download_sequences(output_dir, data)


# pylint: disable=duplicate-code
def list_sequences(
        out_format: str,
        seq_type: str,
        group_name: str,
        sample_ids: List[str] = None,
):
    data = _get_seq_data(
        seq_type,
        group_name,
        sample_ids,
    )
    print_dataframe(
        data,
        out_format,
    )


@logger_wraps()
def purge_sequence(sample_id: str, seq_type: str, skip: bool, force: bool, delete_all: bool):
    custom_headers = {}
    _set_mode_header(custom_headers, force, skip)
    api_path = "/".join([SEQUENCE_PATH, SEQUENCE_BY_SAMPLE_PATH, sample_id, seq_type])

    if delete_all:
        api_path = api_path + '?deleteAll=true'

    api_delete(
        path=api_path,
        custom_headers=custom_headers
    )

def _build_headers(seq_type, csv_row, force, skip):
    # seq type
    headers = {
        SEQTYPE_HEADER: seq_type.value,
    }
    # Put all values from CSV row in headers (Seq_ID and file paths)
    for column in csv_row.index:
        if column==SEQ_ID_CSV:
            headers[SEQ_ID_HEADER] = csv_row[column]
        else:
            headers[HEADER_MAP[column]] = os.path.basename(csv_row[column])
    _set_mode_header(headers, force, skip)
    return headers

def _set_mode_header(headers, force, skip):
    assert not (skip and force)
    if skip:
        headers[MODE_HEADER] = MODE_SKIP
    if force:
        headers[MODE_HEADER] = MODE_OVERWRITE

def _check_csv_files(csv_row: pd.Series, messages: List[Dict]):
    for column in csv_row.index:
        if column==SEQ_ID_CSV:
            continue
        if not os.path.isfile(csv_row[column]):
            messages.append(create_response_object(
                f'File {csv_row[column]} not found',
                RESPONSE_TYPE_ERROR
            ))

def _get_files_from_csv_paths(csv_row: pd.Series, seq_type: SeqType) -> List[SeqFile]:
    sample_files = []
    columns = _csv_columns(seq_type)
    seq_id = csv_row[SEQ_ID_CSV]
    for column in columns:
        # We assume everything in the CSV that's not the Seq_ID is a file path
        if column==SEQ_ID_CSV:
            continue
        contig_rename_id = seq_id if seq_type==SeqType.FASTA_ASM else None
        file = _get_file(csv_row[column], contig_rename_id)
        sample_files.append(file)
    return sample_files

def _get_file(filepath: str, contig_rename_id=None) -> SeqFile:
    # pylint: disable=consider-using-with
    file = open(filepath, 'rb')
    filename = os.path.basename(file.name)
    if contig_rename_id is not None:
        logger.info(f"Renaming contigs in {filename} to include Seq_ID {contig_rename_id}")
        file = _rename_fasta_asm_contigs(file, contig_rename_id)
    return SeqFile(
        multipart=('files[]', (filename, file)),
        sha256=hashlib.sha256(file.read()).hexdigest(),
        filename=filename,
    )

def _rename_fasta_asm_contigs(file: BufferedReader, seq_id: str) -> BufferedReader:
    buffer = BytesIO()
    for line in file:
        linestr = line.decode('utf-8')
        if linestr.startswith('>') and not linestr.startswith(f'>{seq_id}.'):
            linestr = f'>{seq_id}.{linestr[1:]}'
        buffer.write(linestr.encode('utf-8'))
        # else:
        #     buffer.write(line)
    buffer.seek(0)
    file.close()
    return buffer
