import os
import glob

import pytest

from ete_cmd_bricks import (
    _create_field_if_not_exists,
    _create_org,
    _create_group,
    _upload_min_metadata,
    _upload_fasta_cns_file)

from ete_utils import (
    _new_identifier,
    seq_id_field_name,
    _mk_temp_dir,
    _clone_cns_fasta_file)

from test.utils.austrakka_test_cli import AusTrakkaTestCli


class TestSeqGetCommand:
    ext_map = {
        'fasta-cns': 'fasta',
        'fasta-asm': 'fasta',
        'fastq-ill-se': 'fastq',
        'fastq-ill-pe': 'fastq',
        'fastq-ont': 'fastq',
    }
    
    
    @pytest.fixture(autouse=True)
    def _use_cli(self, austrakka_test_cli: AusTrakkaTestCli):
        self.cli = austrakka_test_cli

    def test_get__given_both_seq_id_and_group_are_not_specified__expect_cli_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'fasta-cns',
            '-o',
            temp_dir,
        ])
        
        # Assert
        assert result.exit_code != 0, f'The seq get command should fail: {result.output}'
        assert ("You must provide at least one of these arguments: "
                "`group-name, seq-id`.") in result.output
    
    
    def test_get__given_no_output_dir__expect_cli_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)

        # Act
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'fasta-cns',
            '-s',
            seq_id,
        ])

        # Assert
        assert result.exit_code != 0, f'The seq get command should fail: {result.output}'
        assert "Missing option '-o' / '--outdir'." in result.output
    
    
    def test_get__given_seq_type_is_not_specified__expect_cli_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        result = self.cli.invoke([
            'seq',
            'get',
            '-s',
            seq_id,
            '-o',
            temp_dir,
        ])

        # Assert
        assert result.exit_code != 0, f'The seq get command should fail: {result.output}'
        assert "Missing option '-t' / '--type'." in result.output
    
    
    def test_get__given_both_group_name_and_seq_id_are_specified__expect_cli_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'fasta-cns',
            '-s',
            seq_id,
            '-g',
            shared_group,
            '-o',
            temp_dir,
        ])

        # Assert
        assert result.exit_code != 0, f'The seq get command should fail: {result.output}'
        assert "`seq-id` is mutually exclusive with `group-name`." in result.output
    
    
    def test_get__given_seq_type_is_not_supported__expect_cli_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'BLAH-BLAH-TYPE',
            '-s',
            seq_id,
            '-o',
            temp_dir,
        ])

        # Assert
        assert result.exit_code != 0, f'The seq get command should fail: {result.output}'
        assert "Invalid value for '-t' / '--type': 'BLAH-BLAH-TYPE'" in result.output
    
    
    def test_get__given_seq_id_does_not_exist__expect_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        unknown_seq_id = f'seq-{_new_identifier(10)}'
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'fasta-cns',
            '-s',
            unknown_seq_id,
            '-o',
            temp_dir,
        ])

        # Assert
        assert result.exit_code != 0, f'The seq get command should fail: {result.output}'
        assert f"Sample {unknown_seq_id} not found." in str(result)
    
    
    def test_get__given_seq_id_exists_and_seq_type_matches_the_request__expect_files_downloaded(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'fasta-cns',
            '-s',
            seq_id,
            '-o',
            temp_dir,
        ])
    
        # Assert
        assert result.exit_code == 0, f'The seq get command should succeed: {result.output}'
        self._assert_single_file_downloads_exists([seq_id], 'fasta-cns', temp_dir)

    
    def test_get__given_seq_id_exists_and_seq_type_does_not_match_the_request__expect_no_download(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'fastq-ill-pe',
            '-s',
            seq_id,
            '-o',
            temp_dir,
        ])

        # Assert
        assert result.exit_code == 0, f'The seq get command should succeed: {result.output}'
        assert f"Skipped samples with no available sequences: {seq_id}" in result.output
    
    
    def test_get__given_group_does_not_exist__expect_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        unknown_group = f'sg-{_new_identifier(10)}'
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'fasta-cns',
            '-g',
            unknown_group,
            '-o',
            temp_dir,
        ])

        # Assert
        assert result.exit_code != 0, f'The seq get command should fail: {result.output}'
        assert f"Group {unknown_group} not found" in str(result)
    
    
    def test_get__given_group_exists_and_seq_type_matches_the_request__expect_files_downloaded(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'fasta-cns',
            '-g',
            owner_group,
            '-o',
            temp_dir,
        ])

        # Assert
        assert result.exit_code == 0, f'The seq get command should succeed: {result.output}'
        self._assert_single_file_downloads_exists([seq_id], 'fasta-cns', temp_dir)
    
    
    def test_get__given_group_exists_and_seq_type_does_not_match_the_request__expect_no_download(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_group = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name)
        temp_dir = _mk_temp_dir()

        # Act
        result = self.cli.invoke([
            'seq',
            'get',
            '-t',
            'fastq-ill-pe',
            '-g',
            shared_group,
            '-o',
            temp_dir,
        ])

        # Assert
        assert result.exit_code == 0, f'The seq get command should succeed: {result.output}'
        assert len(os.listdir(temp_dir)) == 0, f'Expected directory to be empty, but found: {os.listdir(temp_dir)}'


    def _assert_single_file_downloads_exists(self, seq_ids: list[str], seq_type, temp_dir):
        ext = TestSeqGetCommand.ext_map
        for seq_id in seq_ids:
            pattern = f'{temp_dir}/{seq_id}/{seq_type}/{seq_id}_*.{ext[seq_type]}'
            matching_files = glob.glob(pattern)
            assert len(matching_files) > 0, \
                f'The output directory should contain files matching the pattern: {pattern}'
        
            # If you need to work with the actual file(s) that match the pattern:
            for file_path in matching_files:
                # Do something with each matching file
                assert os.path.exists(file_path) is True