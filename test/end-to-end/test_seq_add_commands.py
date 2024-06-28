import json
import os
import string
import random
import pandas as pd

from click.testing import CliRunner
from austrakka.main import get_cli


seq_id_field_name = 'Seq_ID'
owner_group_field_name = 'Owner_group'
shared_groups_field_name = 'Shared_groups'
temp_test_dir = 'tmp_test_data/'


class TestSeqAddCommands:
    runner = CliRunner()

    def test_seq_add_fasta_asm__given_sample_has_no_prior_asm_sequences__expect_success_without_needing_skip_or_force(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'
        shared_group = f'sg-{_new_identifier(10)}'
        proforma_name = f'{_new_identifier(10)}'

        _create_field_if_not_exists(self.runner, seq_id_field_name)
        _create_field_if_not_exists(self.runner, owner_group_field_name)
        _create_field_if_not_exists(self.runner, shared_groups_field_name)
        _create_min_proforma(self.runner, proforma_name)
        _create_org(self.runner, org_name)
        _create_group(self.runner, shared_group)

        temp_file_path = _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        # Act
        tmp_fasta_csv_file_path = _upload_fasta_asm_file(self.runner, 'test/test-assets/sequences/XYZ004.fasta', seq_id)

        # Assert
        result = _get_seq_by_group(self.runner, shared_group)
        assert len(result) == 1, f'Failed to add fasta asm file to sequence: {result}'

        # Cleanup
        os.remove(temp_file_path)
        os.remove(tmp_fasta_csv_file_path)


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


def _save_to_test_dir(content: str) -> str:
    temp_file_name = f'{_new_identifier(10)}.csv'
    tmp_file_path = f'{temp_test_dir}{temp_file_name}'

    if not os.path.exists(temp_test_dir):
        os.makedirs(temp_test_dir)

    with open(f'{tmp_file_path}', 'w') as file:
        file.write(content)

    return tmp_file_path


def _get_seq_by_group(runner: CliRunner, group: str):
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


def _create_fasta_csv(seq_id: str, fasta_file_path: str) -> str:
    csv = f'{seq_id_field_name},filepath\n'
    csv += f'{seq_id},{fasta_file_path}\n'
    return _save_to_test_dir(csv)


def _invoke(runner: CliRunner, args):
    global_options = ['--verify_cert', 'false', '--uri', 'https://localhost:5001']
    combined_args = global_options + args
    return runner.invoke(get_cli(), combined_args)


def _new_identifier(n: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
