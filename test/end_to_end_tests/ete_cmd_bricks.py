import json
import tempfile

from click.testing import CliRunner
from ete_utils import _save_to_test_dir, _create_single_seq_csv, _new_identifier, _create_paired_seq_csv
from ete_constants import seq_id_field_name, owner_group_field_name, shared_groups_field_name
from test.utils.austrakka_test_cli import AusTrakkaTestCli


def _sample_unshare(cli: AusTrakkaTestCli, seq_id: str, group_name: str):
    result = cli.invoke([
        'sample',
        'unshare',
        '-s', seq_id,
        '-g', group_name
    ])

    assert result.exit_code == 0, f'Failed to unshare sequence {seq_id} from group {group_name} as part of test setup: {result.output}'


def _seq_sync_get(
        cli: AusTrakkaTestCli,
        group: str,
        output_dir: str,
        seq_type: str,
        recalculate_hash: bool = False,
        assert_success: bool = False,):

    args = [
        'seq',
        'sync',
        'get',
        '-g', group,
        '-o', output_dir,
        '-t', seq_type
    ]

    if recalculate_hash:
        args.append('--recalculate-hashes')

    result = cli.invoke(args)

    if assert_success:
        assert result.exit_code == 0, f'Failed to sync get for group {group} as part of test setup: {result.output}'
    return result


def _upload_fastq_ill_se_file(
        cli: AusTrakkaTestCli,
        seq_id: str,
        fastq_file_path: str,
        skip: bool = False,
        force: bool = False) -> str:

    temp_csv_file_path = _create_single_seq_csv(seq_id, fastq_file_path)

    args = [
        'seq',
        'add',
        'fastq-ill-se',
        temp_csv_file_path
    ]

    if skip:
        args.append('--skip')

    if force:
        args.append('--force')

    result = cli.invoke(args)
    assert result.exit_code == 0, (f'Failed to upload fastq ill se file {fastq_file_path}, '
                                   f'with generated csv: {temp_csv_file_path}  as part of '
                                   f'test setup: {result.output}')
    return temp_csv_file_path


def _upload_fastq_ill_pe_file(
        cli: AusTrakkaTestCli,
        seq_id: str,
        fastq_file_path1: str,
        fastq_file_path2: str,
        skip: bool = False,
        force: bool = False) -> str:

    temp_csv_file_path = _create_paired_seq_csv(seq_id, fastq_file_path1, fastq_file_path2)

    args = [
        'seq',
        'add',
        'fastq-ill-pe',
        temp_csv_file_path
    ]

    if skip:
        args.append('--skip')

    if force:
        args.append('--force')

    result = cli.invoke(args)
    assert result.exit_code == 0, (f'Failed to upload fastq ill pe file {fastq_file_path1} & '
                                   f'{fastq_file_path2}, with generated csv: {temp_csv_file_path} '
                                   f'as part of test setup: {result.output}')
    return temp_csv_file_path


def _upload_fasta_asm_file(
        cli: AusTrakkaTestCli,
        fasta_file_path:
        str, seq_id: str,
        skip: bool = False,
        force: bool = False) -> str:

    temp_csv_file_path = _create_single_seq_csv(seq_id, fasta_file_path)

    args = [
        'seq',
        'add',
        'fasta-asm',
        temp_csv_file_path
    ]

    if skip:
        args.append('--skip')

    if force:
        args.append('--force')

    result = cli.invoke(args)
    assert result.exit_code == 0, f'Failed to upload fasta asm file {fasta_file_path} as part of test setup: {result.output}'
    return temp_csv_file_path


def _upload_fasta_cns_file(
        cli: AusTrakkaTestCli,
        fasta_file_path: str,
        skip: bool = False,
        force: bool = False):

    args = [
        'seq',
        'add',
        'fasta-cns',
        fasta_file_path
    ]

    if skip:
        args.append('--skip')

    if force:
        args.append('--force')

    result = cli.invoke(args)
    assert result.exit_code == 0, f'Failed to upload fasta cns file {fasta_file_path} as part of test setup: {result.output}'


def _upload_min_metadata(
        cli: AusTrakkaTestCli,
        proforma: str,
        seq_ids: list[str],
        owner_group: str,
        shared_groups: list[str]) -> str:

    metadata = _create_csv_content(owner_group, seq_ids, shared_groups)
    temp_file_path = _save_to_test_dir(metadata)

    result = cli.invoke([
        'metadata',
        'add',
        '-p',
        proforma,
        temp_file_path
    ])

    assert result.exit_code == 0, f'Failed to upload minimal metadata as part of test setup: {result.output}'
    return temp_file_path


def _create_csv_content(owner_group, seq_ids, shared_groups) -> str:
    csv = f'{seq_id_field_name},{owner_group_field_name},{shared_groups_field_name}\n'
    for seq_id in seq_ids:
        csv += f'{seq_id},{owner_group},{";".join(shared_groups)}\n'

    return csv


def _create_project(cli: AusTrakkaTestCli, name: str):
    result = cli.invoke([
        'project',
        'add',
        '-a',
        name,
        '-n',
        name,
        '-d',
        'Project for testing'
    ])

    assert result.exit_code == 0, f'Failed to create project {name} as part of test setup: {result.output}'


def _create_group(cli: AusTrakkaTestCli, name: str):
    result = cli.invoke([
        'group',
        'add',
        '-n',
        name,
    ])

    assert result.exit_code == 0, f'Failed to create group {name} as part of test setup: {result.output}'


def _create_min_proforma(
        cli: AusTrakkaTestCli,
        name: str,
        required_fields: list[str] = None,
        optional_fields: list[str] = None):

    args = [
        'proforma',
        'add',
        '-a',
        name,
        '-n',
        name,
        '-d',
        'Min proforma for testing',
        '-req',
        seq_id_field_name,
        '-req',
        owner_group_field_name,
        '-opt',
        shared_groups_field_name,
    ]

    if required_fields:
        for field in required_fields:
            _create_field_if_not_exists(cli, field)
            args.extend(['-req', field])

    if optional_fields:
        for field in optional_fields:
            _create_field_if_not_exists(cli, field)
            args.extend(['-opt', field])

    result = cli.invoke(args)

    assert result.exit_code == 0, f'Failed to create min proforma {name} as part of test setup: {result.output}'


def _create_field_if_not_exists(cli: AusTrakkaTestCli, field_name):
    result = cli.invoke([
        'field',
        'list',
        '-f',
        'json',
    ])

    assert result.exit_code == 0, f'Failed to list fields as part of test setup: {result.output}'

    # parse json array to find field_name matching "columnName" in the json
    fields = json.loads(result.output)
    if field_name.casefold() not in [field['columnName'].casefold() for field in fields]:
        result = cli.invoke([
            'field',
            'add',
            '-n',
            field_name,
            '-ft',
            'string'])

        assert result.exit_code == 0, f'Failed to create field {field_name} as part of test setup: {result.output}'


def _create_org(cli: AusTrakkaTestCli, name: str):
    result = cli.invoke([
        'org',
        'add',
        '-a',
        name,
        '-n',
        name,
    ])

    assert result.exit_code == 0, f'Failed to create org {name} as part of test setup: {result.output}'


def _list_seq_by_group(cli: AusTrakkaTestCli, group: str):
    result = cli.invoke([
        'seq',
        'list',
        '-g',
        group,
        '-f',
        'json'
    ])

    assert result.exit_code == 0, f'Failed to list sequences by group {group} as part of test setup: {result.output}'
    return json.loads(result.output)
