import os
import string
import random
import tempfile

from click.testing import CliRunner
from austrakka.main import get_cli


seq_id_field_name = 'Seq_ID'
owner_group_field_name = 'Owner_group'
shared_groups_field_name = 'Shared_groups'


def _save_to_test_dir(content: str) -> str:
    temp_dir = tempfile.gettempdir()
    # if temp_dir does not end with a slash, add one
    if not temp_dir.endswith('/'):
        temp_dir += '/'

    print(f'Temp dir: {temp_dir}')

    temp_file_name = f'{_new_identifier(10)}.csv'
    tmp_file_path = f'{temp_dir}{temp_file_name}'

    with open(f'{tmp_file_path}', 'w') as file:
        file.write(content)

    return tmp_file_path


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
