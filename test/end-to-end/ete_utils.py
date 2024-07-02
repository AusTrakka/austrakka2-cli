import json
import os
import string
import random
import tempfile

from click.testing import CliRunner
from austrakka.main import get_cli


seq_id_field_name = 'Seq_ID'
owner_group_field_name = 'Owner_group'
shared_groups_field_name = 'Shared_groups'


def _clone_cns_fasta_file(
        original_file_path: str, 
        old_seq_id: str, 
        seq_id_override: str) -> str:

    with open(original_file_path, 'r') as file:
        content = file.read()

    temp_dir = tempfile.gettempdir()
    temp_file_name = f'{seq_id_override}.fasta'
    temp_file_path = f'{temp_dir}/{temp_file_name}'

    content = content.replace(old_seq_id, seq_id_override)
    with open(temp_file_path, 'w') as file:
        file.write(content)

    return temp_file_path


def _mk_temp_dir() -> str:
    temp_dir = tempfile.gettempdir()
    rand_subdir = _new_identifier(10)
    full_output_dir = os.path.join(temp_dir, rand_subdir)

    if not os.path.exists(full_output_dir):
        os.makedirs(full_output_dir)

    return full_output_dir


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


def _read_sync_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding='UTF-8') as file:
            return json.load(file)
    else:
        return {}


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
