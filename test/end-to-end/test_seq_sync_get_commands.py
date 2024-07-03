import os
import shutil

import pandas as pd
import pytest
from click.testing import CliRunner

from ete_cmd_bricks import (
    _create_field_if_not_exists,
    _create_min_proforma,
    _create_org,
    _create_group,
    _upload_fasta_asm_file,
    _upload_min_metadata,
    _seq_sync_get,
    _upload_fasta_cns_file,
    _sample_unshare,
    _upload_fastq_ill_pe_file,
    _upload_fastq_ill_se_file)

from ete_utils import (
    _new_identifier,
    seq_id_field_name,
    owner_group_field_name,
    shared_groups_field_name,
    _mk_temp_dir,
    _clone_cns_fasta_file,
    _read_sync_state,
    _calc_hash,
    _undo_fasta_asm_transform,
    _textwrap)


class TestSeqSyncGetCommands:
    runner = CliRunner()

    @pytest.mark.skip(reason="Not implemented")
    def test_sync_migrate__given_existing_fasta__expect_migration_to_fasta_cns_with_correct_files_and_contents(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="Not implemented")
    def test_sync_migrate__given_existing_fastq__expect_migration_to_fastq_ill_pe_with_correct_files_and_contents(self):
        raise NotImplementedError

    @pytest.mark.parametrize("seq_type", ['fasta-asm', 'fasta-cns', 'fastq-ill-pe', 'fastq-ill-se'])
    def test_sync_get__given_group_has_no_sequences__expect_no_sequence_downloaded(self, seq_type):
        # Arrange
        shared_group = f'sg-{_new_identifier(10)}'
        _create_group(self.runner, shared_group)
        temp_dir = _mk_temp_dir()

        # Act
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        self.assert_no_seq_dirs(temp_dir)
        self.assert_manifest_file_exists(seq_type, temp_dir)

    @pytest.mark.parametrize("seq_type", ['fasta-asm', 'fasta-cns', 'fastq-ill-pe', 'fastq-ill-se'])
    def test_sync_get__given_group_has_no_sequences__expect_current_state_is__up_to_date(self, seq_type):
        # Arrange
        shared_group = f'sg-{_new_identifier(10)}'
        _create_group(self.runner, shared_group)
        temp_dir = _mk_temp_dir()

        # Act
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_state'] == 'UP_TO_DATE', \
            f'The current state should be up_to_date: {state_dict}'

    @pytest.mark.parametrize("seq_type", ['fasta-asm', 'fasta-cns', 'fastq-ill-pe', 'fastq-ill-se'])
    def test_sync_get__given_group_has_no_sequences__expect_current_action_is__pulling_manifest(self, seq_type):
        # Arrange
        shared_group = f'sg-{_new_identifier(10)}'
        _create_group(self.runner, shared_group)
        temp_dir = _mk_temp_dir()

        # Act
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_action'] == 'set-state/pulling-manifest', \
            f'The current action should be set-state/pulling-manifest: {state_dict}'

    @pytest.mark.parametrize("seq_type", ['fasta-asm', 'fasta-cns', 'fastq-ill-pe', 'fastq-ill-se'])
    def test_sync_get__given_group_has_sequences__expect_correct_state_file_name_and_contents(self, seq_type):
        # Arrange
        shared_group = f'sg-{_new_identifier(10)}'
        _create_group(self.runner, shared_group)
        temp_dir = _mk_temp_dir()

        # Act
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')

        assert state_dict['current_state'] == 'UP_TO_DATE', \
            f'The current state should be up_to_date: {state_dict}'

        assert state_dict['current_action'] == 'set-state/pulling-manifest', \
            f'The current action should be set-state/pulling-manifest: {state_dict}'

        assert state_dict['sync_state_file'] == f'sync-state-{seq_type}.json', \
            f'The sync state file should be sync-state-{seq_type}.json: {state_dict}'

        assert state_dict['manifest'] == f'manifest-{seq_type}.csv', \
            f'The manifest file should be manifest-{seq_type}.csv: {state_dict}'

        assert state_dict['output_dir'] == temp_dir, \
            f'The output directory should be {temp_dir}: {state_dict}'

        assert state_dict['seq_type'] == seq_type, \
            f'The sequence type should be {seq_type}: {state_dict}'

        assert state_dict['group_name'] == shared_group, \
            f'The group name should be {shared_group}: {state_dict}'

        assert state_dict['recalculate_hash'] == False, \
            f'The recalculate hash should be False: {state_dict}'

        assert state_dict['trash_dir'] == '.trash', \
            f'The trash directory should be .trash: {state_dict}'

        assert state_dict['download_batch_size'] == 1, \
            f'The download batch size should be 1: {state_dict}'

        assert state_dict['obsolete_objects_file'] == f'delete-targets-{seq_type}.csv', \
            f'The obsolete objects file should be delete-targets-{seq_type}.csv: {state_dict}'

        assert state_dict['intermediate_manifest_file'] == f'intermediate-manifest-{seq_type}.csv', \
            f'The intermediate manifest file should be intermediate-manifest-{seq_type}.csv: {state_dict}'

    def test_sync_get__given_group_has_removed_fasta_cns_sequences__expect_fasta_cns_moved_to_trash_and_other_sequences_unchanged(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        # Fill the output dir with asm as if it was previously downloaded
        _upload_fasta_asm_file(self.runner, 'test/test-assets/sequences/asm/XYZ-asm-004.fasta', seq_id)
        temp_dir = _mk_temp_dir()
        fasta_asm_type = 'fasta-asm'
        _seq_sync_get(self.runner, shared_group, temp_dir, fasta_asm_type)
        self.assert_state_file_exists(fasta_asm_type, temp_dir)
        self.assert_manifest_file_exists(fasta_asm_type, temp_dir)
        self.assert_has_seq_dirs(f'{temp_dir}/{seq_id}/{fasta_asm_type}', 1)

        # Upload a fasta cns file, so it can be removed as per the test case
        cns_fasta_path = _clone_cns_fasta_file(
            'test/test-assets/sequences/cns/ABC-cns-001.fasta',
            'SEQ_ABC-cns-001',
            seq_id)

        _upload_fasta_cns_file(self.runner, cns_fasta_path)
        fasta_cns_type = 'fasta-cns'
        _seq_sync_get(self.runner, shared_group, temp_dir, fasta_cns_type)
        self.assert_state_file_exists(fasta_cns_type, temp_dir)
        self.assert_manifest_file_exists(fasta_cns_type, temp_dir)
        self.assert_has_seq_dirs(f'{temp_dir}/{seq_id}/{fasta_cns_type}', 1)

        # Act
        _sample_unshare(self.runner, seq_id, shared_group)
        _seq_sync_get(self.runner, shared_group, temp_dir, 'fasta-cns')

        # Assert
        # CNS content should be zero
        self.assert_state_file_exists(fasta_cns_type, temp_dir)
        self.assert_manifest_file_exists(fasta_cns_type, temp_dir)
        seq_dir = f'{temp_dir}/{seq_id}'
        cns_dir = f'{temp_dir}/{seq_id}/{fasta_cns_type}'
        assert os.path.exists(seq_dir) is True, (f'The output directory should contain a sub directory '
                                                 f'for the sequence: {seq_dir}')

        assert os.path.exists(cns_dir) is False, f'The sequence directory should have no fasta-cns subdir: {cns_dir}'
        assert os.path.exists(f'{temp_dir}/.trash/{seq_id}/{fasta_cns_type}') is True, \
            (f'The output directory should contain a trash directory for the sequence: '
             f'{temp_dir}/.trash/{seq_id}/{fasta_cns_type}')

        trash_content = os.listdir(f'{temp_dir}/.trash/{seq_id}/{fasta_cns_type}')
        seq_file = trash_content[0]
        assert seq_file.startswith(seq_id) and seq_file.endswith('.fasta'), \
            f'The trash directory should contain a fasta file: {trash_content}'

        # ASM content should be one (untouched)
        self.assert_state_file_exists(fasta_asm_type, temp_dir)
        self.assert_manifest_file_exists(fasta_asm_type, temp_dir)
        self.assert_has_seq_dirs(f'{temp_dir}/{seq_id}/{fasta_asm_type}', 1)

    @pytest.mark.parametrize("original_file_dir, original_file_name", [
        ('test/test-assets/sequences/asm/', 'XYZ-asm-004.fasta'),
        ('test/test-assets/sequences/asm/', 'XYZ-asm-004-desc.fasta')])
    def test_sync_get__given_group_has_fasta_asm_sequences_and_download_was_successful__expect_hashes_of_downloads_to_match_original_with_transform(
            self,
            original_file_dir,
            original_file_name):

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

        original_file = f'{original_file_dir}{original_file_name}'

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        _upload_fasta_asm_file(self.runner, original_file, seq_id)

        # Act
        temp_dir = _mk_temp_dir()
        print(f'Temp dir: {temp_dir}')
        seq_type = 'fasta-asm'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        # Undo transform to the downloaded file. It should have the same hash as the original
        original_hash = _calc_hash(original_file)
        clone_path = f'{temp_dir}/clone-{original_file_name}'

        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_file = [f for f in dir_contents if f.endswith('.fasta')][0]
        downloaded_file_path = f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_file}'
        shutil.copyfile(downloaded_file_path, clone_path)

        _undo_fasta_asm_transform(clone_path, seq_id)

        clone_hash = _calc_hash(clone_path)
        assert original_hash == clone_hash, \
            (f'The hash of the undone transformed downloaded file should match the original: '
             f'{original_hash} != {clone_hash}')

        # Check the downloaded file against the hash in the manifest.
        df = pd.read_csv(f'{temp_dir}/manifest-{seq_type}.csv')
        hash_in_manifest = df.loc[df['Seq_ID'] == seq_id]['HASH_FASTA-ASM'].values[0].casefold()
        downloaded_file_hash = _calc_hash(downloaded_file_path)

        assert downloaded_file_hash == hash_in_manifest, \
            'The hash of the downloaded fasta asm file should match the hash declared in the manifest.'

    def test_sync_get__given_group_has_fastq_ill_pe_sequences_and_download_was_successful__expect_hashes_of_downloads_to_match_original(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file1 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r1.fastq'
        original_file2 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r2.fastq'
        _upload_fastq_ill_pe_file(self.runner, seq_id, original_file1, original_file2)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-pe'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        original_hash1 = _calc_hash(original_file1)
        original_hash2 = _calc_hash(original_file2)

        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_r1 = [f for f in dir_contents if '_R1' in f and f.endswith('.fastq')][0]
        downloaded_r2 = [f for f in dir_contents if '_R2' in f and f.endswith('.fastq')][0]

        downloaded_r1_hash = _calc_hash(f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_r1}')
        downloaded_r2_hash = _calc_hash(f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_r2}')

        # read the expected hash from the manifest file. All three
        # (original, downloaded, manifest) should match
        df = pd.read_csv(f'{temp_dir}/manifest-{seq_type}.csv')
        r1_hash_in_manifest = df.loc[df['Seq_ID'] == seq_id]['HASH_FASTQ-ILL-PE_R1'].values[0].casefold()
        r2_hash_in_manifest = df.loc[df['Seq_ID'] == seq_id]['HASH_FASTQ-ILL-PE_R2'].values[0].casefold()

        assert original_hash1 == downloaded_r1_hash and downloaded_r1_hash == r1_hash_in_manifest, \
            (f'The hash of the downloaded r1 file should match the original: '
             f'{original_hash1} != {downloaded_r1_hash}')

        assert original_hash2 == downloaded_r2_hash and downloaded_r2_hash == r2_hash_in_manifest, \
            (f'The hash of the downloaded r2 file should match the original: '
             f'{original_hash2} != {downloaded_r2_hash}')

    def test_sync_get__given_group_has_fastq_ill_se_sequences_and_download_was_successful__expect_hashes_of_downloads_to_match_original(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        # Undo transform to the downloaded file. It should have the same hash as the original
        original_hash = _calc_hash(original_file)
        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_file = [f for f in dir_contents if f.endswith('.fastq')][0]
        downloaded_file_hash = _calc_hash(f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_file}')

        # read the expected hash from the manifest file. All three
        # (original, downloaded, manifest) should match
        df = pd.read_csv(f'{temp_dir}/manifest-{seq_type}.csv')
        hash_in_manifest = df.loc[df['Seq_ID'] == seq_id]['HASH_FASTQ-ILL-SE'].values[0].casefold()

        assert original_hash == downloaded_file_hash and downloaded_file_hash == hash_in_manifest, \
            (f'The hash of the downloaded ill-se file should match the original: '
             f'{original_hash} != {downloaded_file_hash}')

    @pytest.mark.parametrize("original_file", [
        'test/test-assets/sequences/cns/ABC-cns-001.fasta',
        'test/test-assets/sequences/cns/ABC-cns-001-desc.fasta'])
    def test_sync_get__given_group_has_fasta_cns_sequences_and_download_was_successful__expect_hashes_of_downloads_to_match_original(
            self,
            original_file):

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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            'SEQ_ABC-cns-001',
            seq_id)

        _upload_fasta_cns_file(self.runner, cns_fasta_path)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fasta-cns'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        # During upload, the cli would have line wrapped at 60 char. In order to compare
        # the hashes, we need to word wrap the original file as well.
        wrap_adjusted_file_path = f'{cns_fasta_path}-adjusted.bak'
        _textwrap(60, cns_fasta_path, wrap_adjusted_file_path)
        line_wrapped_original_hash = _calc_hash(wrap_adjusted_file_path)

        # Get the downloaded file
        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_file = [f for f in dir_contents if f.endswith('.fasta')][0]
        downloaded_file_path = f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_file}'
        downloaded_file_hash = _calc_hash(downloaded_file_path)

        # read the expected hash from the manifest file. All three
        # (original, downloaded, manifest) should match
        df = pd.read_csv(f'{temp_dir}/manifest-{seq_type}.csv')
        hash_in_manifest = df.loc[df['Seq_ID'] == seq_id]['HASH_FASTA-CNS'].values[0].casefold()

        assert line_wrapped_original_hash == downloaded_file_hash and downloaded_file_hash == hash_in_manifest, \
            (f'The hash of the downloaded cns file should match the original: '
             f'{line_wrapped_original_hash} != {downloaded_file_hash}')

    def test_sync_get__given_group_has_fasta_asm_sequences_and_download_was_successful__expect_contigs_are_renamed(self):
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

        original_file_dir = 'test/test-assets/sequences/asm/'
        original_file_name = 'XYZ-asm-004.fasta'
        original_file = f'{original_file_dir}{original_file_name}'

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        _upload_fasta_asm_file(self.runner, original_file, seq_id)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fasta-asm'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        # Undo transform to the downloaded file. It should have the same hash as the original
        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_file = [f for f in dir_contents if f.endswith('.fasta')][0]
        downloaded_file_path = f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_file}'

        with open(downloaded_file_path, 'r') as file:
            first_line = file.readline()
            assert first_line.startswith(f'>{seq_id}.SEQ_XYZ-asm-004'), \
                f'The first line of the downloaded fasta asm file should be renamed to include the Seq_ID: {first_line}'

    def test_sync_get__given_group_has_fasta_asm_sequences_and_download_was_successful__expect_sequences_are_listed_in_manifest(self):
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

        original_file_dir = 'test/test-assets/sequences/asm/'
        original_file_name = 'XYZ-asm-004.fasta'
        original_file = f'{original_file_dir}{original_file_name}'

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        _upload_fasta_asm_file(self.runner, original_file, seq_id)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fasta-asm'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        df = pd.read_csv(f'{temp_dir}/manifest-{seq_type}.csv')
        assert seq_id in df['Seq_ID'].values, f'The Seq_ID should be in the manifest: {df}'

    def test_sync_get__given_group_has_fasta_asm_sequences_and_download_was_successful__expect_current_state_is__up_to_date(self):
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

        original_file_dir = 'test/test-assets/sequences/asm/'
        original_file_name = 'XYZ-asm-004.fasta'
        original_file = f'{original_file_dir}{original_file_name}'

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        _upload_fasta_asm_file(self.runner, original_file, seq_id)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fasta-asm'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_state'] == 'UP_TO_DATE', f'The current state should be up_to_date: {state_dict}'

    def test_sync_get__given_group_has_fasta_asm_sequences_and_download_was_successful__expect_current_action_is__pulling_manifest(self):
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

        original_file_dir = 'test/test-assets/sequences/asm/'
        original_file_name = 'XYZ-asm-004.fasta'
        original_file = f'{original_file_dir}{original_file_name}'

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        _upload_fasta_asm_file(self.runner, original_file, seq_id)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fasta-asm'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_action'] == 'PULLING_MANIFEST', \
            f'The current action should be PULLING_MANIFEST: {state_dict}'

    def test_sync_get__given_group_has_fasta_cns_sequences_and_download_was_successful__expect_sequences_are_listed_in_manifest(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/cns/ABC-cns-001.fasta'

        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            'SEQ_ABC-cns-001',
            seq_id)

        _upload_fasta_cns_file(self.runner, cns_fasta_path)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fasta-cns'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        df = pd.read_csv(f'{temp_dir}/manifest-{seq_type}.csv')
        assert seq_id in df['Seq_ID'].values, f'The Seq_ID should be in the manifest: {df}'
        assert seq_id in df['Seq_ID'].values, f'The Seq_ID should be in the manifest: {df}'

    def test_sync_get__given_group_has_fasta_cns_sequences_and_download_was_successful__expect_current_state_is__up_to_date(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/cns/ABC-cns-001.fasta'

        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            'SEQ_ABC-cns-001',
            seq_id)

        _upload_fasta_cns_file(self.runner, cns_fasta_path)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fasta-cns'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_state'] == 'UP_TO_DATE', f'The current state should be up_to_date: {state_dict}'

    def test_sync_get__given_group_has_fasta_cns_sequences_and_download_was_successful__expect_current_action_is__pulling_manifest(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/cns/ABC-cns-001.fasta'

        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            'SEQ_ABC-cns-001',
            seq_id)

        _upload_fasta_cns_file(self.runner, cns_fasta_path)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fasta-cns'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_action'] == 'PULLING_MANIFEST', \
            f'The current action should be pulling_manifest: {state_dict}'

    def test_sync_get__given_group_has_fastq_ill_pe_sequences_and_download_was_successful__expect_sequences_are_listed_in_manifest(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file1 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r1.fastq'
        original_file2 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r2.fastq'
        _upload_fastq_ill_pe_file(self.runner, seq_id, original_file1, original_file2)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-pe'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        df = pd.read_csv(f'{temp_dir}/manifest-{seq_type}.csv')
        assert seq_id in df['Seq_ID'].values, f'The Seq_ID should be in the manifest: {df}'

    def test_sync_get__given_group_has_fastq_ill_pe_sequences_and_download_was_successful__expect_current_state_is__up_to_date(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file1 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r1.fastq'
        original_file2 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r2.fastq'
        _upload_fastq_ill_pe_file(self.runner, seq_id, original_file1, original_file2)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-pe'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_state'] == 'UP_TO_DATE', f'The current state should be up_to_date: {state_dict}'

    def test_sync_get__given_group_has_fastq_ill_pe_sequences_and_download_was_successful__expect_current_action_is__pulling_manifest(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file1 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r1.fastq'
        original_file2 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r2.fastq'
        _upload_fastq_ill_pe_file(self.runner, seq_id, original_file1, original_file2)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-pe'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_action'] == 'PULLING_MANIFEST', \
            f'The current action should be pulling_manifest: {state_dict}'

    def test_sync_get__given_group_has_fastq_ill_se_sequences_and_download_was_successful__expect_sequences_are_listed_in_manifest(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        df = pd.read_csv(f'{temp_dir}/manifest-{seq_type}.csv')
        assert seq_id in df['Seq_ID'].values, f'The Seq_ID should be in the manifest: {df}'

    def test_sync_get__given_group_has_fastq_ill_se_sequences_and_download_was_successful__expect_current_state_is__up_to_date(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_state'] == 'UP_TO_DATE', f'The current state should be up_to_date: {state_dict}'

    def test_sync_get__given_group_has_fastq_ill_se_sequences_and_download_was_successful__expect_current_action_is__pulling_manifest(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        self.assert_state_file_exists(seq_type, temp_dir)
        state_dict = _read_sync_state(f'{temp_dir}/sync-state-{seq_type}.json')
        assert state_dict['current_action'] == 'PULLING_MANIFEST', \
            f'The current action should be pulling_manifest: {state_dict}'

    def test_sync_get__given_successful_successive_download_of_multiple_sequence_types__expect_multiple_manifest_and_state_files_and_correct_directory_structure(self):
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
        temp_dir = _mk_temp_dir()

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        # Act upload and sync get for two types of sequences
        # FASTQ ILL SE
        original_file1 = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file1)

        seq_type1 = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type1)

        # FASTQ ILL PE
        original_file2 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r1.fastq'
        original_file3 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r2.fastq'
        _upload_fastq_ill_pe_file(self.runner, seq_id, original_file2, original_file3)

        seq_type2 = 'fastq-ill-pe'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type2)

        # Assert
        self.assert_manifest_file_exists(seq_type1, temp_dir)
        self.assert_manifest_file_exists(seq_type2, temp_dir)
        self.assert_state_file_exists(seq_type1, temp_dir)
        self.assert_state_file_exists(seq_type2, temp_dir)

        assert os.path.exists(f'{temp_dir}/{seq_id}/{seq_type1}') is True, \
            f'The output directory should contain a sub directory for the sequence type: {temp_dir}'

        assert os.path.exists(f'{temp_dir}/{seq_id}/{seq_type2}') is True, \
            f'The output directory should contain a sub directory for the sequence type: {temp_dir}'

    def test_sync_get__given_output_dir_was_used_for_group_A_and_now_used_for_group_B__expect_command_is_refused(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'
        shared_group = f'sg-{_new_identifier(10)}'
        shared_group2 = f'sg-{_new_identifier(10)}'
        proforma_name = f'{_new_identifier(10)}'

        _create_field_if_not_exists(self.runner, seq_id_field_name)
        _create_field_if_not_exists(self.runner, owner_group_field_name)
        _create_field_if_not_exists(self.runner, shared_groups_field_name)
        _create_min_proforma(self.runner, proforma_name)
        _create_org(self.runner, org_name)
        _create_group(self.runner, shared_group)
        _create_group(self.runner, shared_group2)

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)
        result = _seq_sync_get(self.runner, shared_group2, temp_dir, seq_type)

        # Assert
        assert result.exit_code == 1, f'The command should be refused: {result.output}'

    def test_sync_get__given_previous_successful_download_and_local_file_is_deleted__expect_file_is_repaired(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # check that the downloaded file exists, and then delete it.
        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_file = [f for f in dir_contents if f.endswith('.fastq')][0]
        downloaded_file_path = f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_file}'
        assert os.path.exists(downloaded_file_path) is True, f'The downloaded file should exist: {downloaded_file_path}'
        os.remove(downloaded_file_path)

        # Re-run the sync get
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        assert os.path.exists(downloaded_file_path) is True, f'The downloaded file should be repaired: {downloaded_file_path}'

        original_hash = _calc_hash(original_file)
        downloaded_file_hash = _calc_hash(downloaded_file_path)
        assert original_hash == downloaded_file_hash, (f'The hash of the downloaded ill-se file should match the '
                                                       f'original: {original_hash} != {downloaded_file_hash}')

    def test_sync_get__given_previous_successful_download_and_local_file_is_altered__expect_file_is_repaired(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # check that the downloaded file exists, and then alter it.
        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_file = [f for f in dir_contents if f.endswith('.fastq')][0]
        downloaded_file_path = f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_file}'
        assert os.path.exists(downloaded_file_path) is True, f'The downloaded file should exist: {downloaded_file_path}'

        with open(downloaded_file_path, 'a') as file:
            file.write('This is a test')

        # Re-run the sync get
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type, recalculate_hash=True)

        # Assert
        assert os.path.exists(downloaded_file_path) is True, f'The downloaded file should be repaired: {downloaded_file_path}'

        original_hash = _calc_hash(original_file)
        downloaded_file_hash = _calc_hash(downloaded_file_path)
        assert original_hash == downloaded_file_hash, (f'The hash of the downloaded ill-se file should match the '
                                                       f'original: {original_hash} != {downloaded_file_hash}')

    def test_sync_get__given_previous_successful_download_and_sample_is_unshared_from_group__expect_local_file_is_moved_to_trash(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Sync the file and that it exists
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # check that the downloaded file exists, and then alter it.
        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_file = [f for f in dir_contents if f.endswith('.fastq')][0]
        downloaded_file_path = f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_file}'
        assert os.path.exists(downloaded_file_path) is True, f'The downloaded file should exist: {downloaded_file_path}'

        # Act
        _sample_unshare(self.runner, seq_id, shared_group)
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        assert os.path.exists(downloaded_file_path) is False, \
            f'The downloaded file should be moved to trash: {downloaded_file_path}'

        trash_content = os.listdir(f'{temp_dir}/.trash/{seq_id}/{seq_type}')
        seq_file = trash_content[0]
        assert seq_file.startswith(seq_id) and seq_file.endswith('.fastq'), \
            f'The trash directory should contain a fastq file: {trash_content}'

    def test_sync_get__given_stray_sequence_files_were_added_to_output_directory_and_the_next_run_is_successful__expect_stray_files_are_moved_to_trash(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # check that the downloaded file exists, and then add stray files.
        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_file = [f for f in dir_contents if f.endswith('.fastq')][0]
        downloaded_file_path = f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_file}'
        assert os.path.exists(downloaded_file_path) is True, f'The downloaded file should exist: {downloaded_file_path}'

        # add stray file
        stray_file1 = f'{temp_dir}/{seq_id}/{seq_type}/seq-8TD25CBOC2_20240703T05413366_bbbbbbbb.fastq'
        with open(stray_file1, 'w') as file:
            file.write('This is a test')

        # Re-run the sync get
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        assert os.path.exists(stray_file1) is False, f'The stray file should be moved to trash: {stray_file1}'
        expected_stray_file_trash_path = f'{temp_dir}/.trash/{seq_id}/{seq_type}/seq-8TD25CBOC2_20240703T05413366_bbbbbbbb.fastq'
        assert os.path.exists(expected_stray_file_trash_path) is True, \
            f'The stray file should be moved to trash: {expected_stray_file_trash_path}'

        # check that the downloaded file is still intact
        assert os.path.exists(downloaded_file_path) is True, f'The downloaded file should exist: {downloaded_file_path}'

    def test_sync_get__given_stray_non_sequence_files_were_added_to_output_directory_and_the_next_run_is_successful__expect_stray_files_left_alone(self):
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

        _upload_min_metadata(
            self.runner,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/ill-se/ill-se-002.fastq'
        _upload_fastq_ill_se_file(self.runner, seq_id, original_file)

        # Act
        temp_dir = _mk_temp_dir()
        seq_type = 'fastq-ill-se'
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # check that the downloaded file exists, and then add stray files.
        dir_contents = os.listdir(f'{temp_dir}/{seq_id}/{seq_type}')
        downloaded_file = [f for f in dir_contents if f.endswith('.fastq')][0]
        downloaded_file_path = f'{temp_dir}/{seq_id}/{seq_type}/{downloaded_file}'
        assert os.path.exists(downloaded_file_path) is True, f'The downloaded file should exist: {downloaded_file_path}'

        # add stray file
        stray_file1 = f'{temp_dir}/{seq_id}/{seq_type}/stray-text-file.txt'
        with open(stray_file1, 'w') as file:
            file.write('This is a test')

        # Re-run the sync get
        _seq_sync_get(self.runner, shared_group, temp_dir, seq_type)

        # Assert
        assert os.path.exists(stray_file1) is True, f'The stray file should left untouched: {stray_file1}'
        expected_stray_file_trash_path = f'{temp_dir}/.trash/{seq_id}/{seq_type}/stray-text-file.txt'
        assert os.path.exists(expected_stray_file_trash_path) is False, \
            f'The stray file should not be moved to trash: {expected_stray_file_trash_path}'

        # check that the downloaded file is still intact
        assert os.path.exists(downloaded_file_path) is True, f'The downloaded file should exist: {downloaded_file_path}'

    def assert_state_file_exists(self, seq_type, temp_dir):
        expected_state_file = f'{temp_dir}/sync-state-{seq_type}.json'
        assert os.path.exists(
            expected_state_file) is True, f'The output directory should contain a state file: {expected_state_file}'

    def assert_manifest_file_exists(self, seq_type, temp_dir):
        expected_manifest_file = f'{temp_dir}/manifest-{seq_type}.csv'
        assert os.path.exists(
            expected_manifest_file) is True, \
            f'The output directory should contain a manifest file: {expected_manifest_file}'

    def assert_no_seq_dirs(self, temp_dir: str):
        sub_dirs = os.listdir(temp_dir)
        seq_sub_dirs = [d for d in sub_dirs
                        if (not d.endswith('.trash') and not d.endswith('.trash/'))
                            and os.path.isdir(os.path.join(temp_dir, d))]
        assert len(
            seq_sub_dirs) == 0, f'The output directory should not contain any sequence sub directories: {sub_dirs}'

    def assert_has_seq_dirs(self, temp_dir: str, expected_seq_dirs: int):
        sub_dirs = os.listdir(temp_dir)
        print(temp_dir)
        seq_sub_dirs = [d for d in sub_dirs
                        if (not d.endswith('.trash') and not d.endswith('.trash/'))]

        print(f'Found seq sub dirs: {seq_sub_dirs}')
        for seq_sub_dir in seq_sub_dirs:
            print(f'Found seq sub dir: {seq_sub_dir}')

        assert len(
            seq_sub_dirs) == expected_seq_dirs, f'The output directory should contain {expected_seq_dirs} sequence sub directories: {sub_dirs}'
