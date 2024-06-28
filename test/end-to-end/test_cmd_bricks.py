import json

from click.testing import CliRunner
from test_utils import _save_to_test_dir, _create_fasta_csv, _invoke
from test_constants import seq_id_field_name, owner_group_field_name, shared_groups_field_name


def _upload_fasta_asm_file(
        runner: CliRunner,
        fasta_file_path:
        str, seq_id: str,
        skip: bool = False,
        force: bool = False) -> str:

    temp_csv_file_path = _create_fasta_csv(seq_id, fasta_file_path)

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

    result = _invoke(runner, args)
    assert result.exit_code == 0, f'Failed to upload fasta asm file {fasta_file_path} as part of test setup: {result.output}'
    return temp_csv_file_path


def _upload_min_metadata(
        runner: CliRunner,
        proforma: str,
        seq_ids: list[str],
        owner_group: str,
        shared_groups: list[str]) -> str:

    metadata = _create_csv_content(owner_group, seq_ids, shared_groups)
    temp_file_path = _save_to_test_dir(metadata)

    result = _invoke(runner, [
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


def _create_project(runner: CliRunner, name: str):
    result = _invoke(runner, [
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


def _create_group(runner: CliRunner, name: str):
    result = _invoke(runner, [
        'group',
        'add',
        '-n',
        name,
    ])

    assert result.exit_code == 0, f'Failed to create group {name} as part of test setup: {result.output}'


def _create_min_proforma(runner: CliRunner, name: str):
    result = _invoke(runner, [
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
    ])

    assert result.exit_code == 0, f'Failed to create min proforma {name} as part of test setup: {result.output}'


def _create_field_if_not_exists(runner: CliRunner, field_name):
    result = _invoke(runner, [
        'field',
        'list',
        '-f',
        'json',
    ])

    assert result.exit_code == 0, f'Failed to list fields as part of test setup: {result.output}'

    # parse json array to find field_name matching "columnName" in the json
    fields = json.loads(result.output)
    if field_name.casefold() not in [field['columnName'].casefold() for field in fields]:
        result = _invoke(runner, [
            'field',
            'add',
            '-n',
            field_name,
            '-ft',
            'string'])

        assert result.exit_code == 0, f'Failed to create field {field_name} as part of test setup: {result.output}'


def _create_org(runner: CliRunner, name: str):
    result = _invoke(runner, [
        'org',
        'add',
        '-a',
        name,
        '-n',
        name,
    ])

    assert result.exit_code == 0, f'Failed to create org {name} as part of test setup: {result.output}'


def _list_seq_by_group(runner: CliRunner, group: str):
    result = _invoke(runner, [
        'seq',
        'list',
        '-g',
        group,
        '-f',
        'json'
    ])

    assert result.exit_code == 0, f'Failed to list sequences by group {group} as part of test setup: {result.output}'
    return json.loads(result.output)
