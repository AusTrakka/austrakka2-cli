import pytest

from ete_cmd_bricks import (
    _create_field_if_not_exists,
    _create_min_proforma,
    _create_org,
    _create_group,
    _upload_min_metadata,
    _upload_fasta_cns_file,
    _list_seq_by_group)

from ete_utils import (
    _new_identifier,
    seq_id_field_name,
    owner_group_field_name,
    shared_groups_field_name,
    _clone_cns_fasta_file)

from test.utils.austrakka_test_cli import AusTrakkaTestCli


class TestSeqPurgeCommand:
    @pytest.fixture(autouse=True)
    def _use_cli(self, austrakka_test_cli: AusTrakkaTestCli):
        self.cli = austrakka_test_cli
    
    def test_purge__given_seq_type_not_specified__expect_cli_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'
        shared_group = f'sg-{_new_identifier(10)}'
        proforma_name = f'{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_field_if_not_exists(self.cli, owner_group_field_name)
        _create_field_if_not_exists(self.cli, shared_groups_field_name)
        _create_min_proforma(self.cli, proforma_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        _upload_min_metadata(
            self.cli,
            proforma_name,
            [seq_id, seq_id2],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])
    
        _upload_fasta_cns_file(self.cli, cns_fasta_path)

        # Act
        result = self.cli.invoke([
            'seq',
            'purge',
            '-s',
            seq_id,
            '--force',
            '--delete-all'
        ])

        # Assert
        assert result.exit_code != 0, f'The seq purge command should fail: {result.output}'
        assert "Missing option '-t' / '--type'." in result.output


    def test_purge__given_sequence_is_still_active_and_delete_all_flag_is_not_present__expect_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'
        shared_group = f'sg-{_new_identifier(10)}'
        proforma_name = f'{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_field_if_not_exists(self.cli, owner_group_field_name)
        _create_field_if_not_exists(self.cli, shared_groups_field_name)
        _create_min_proforma(self.cli, proforma_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        _upload_min_metadata(
            self.cli,
            proforma_name,
            [seq_id, seq_id2],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path)

        # Act
        result = self.cli.invoke([
            'seq',
            'purge',
            '-s',
            seq_id,
            '--force',
            '-t',
            'fasta-cns',
        ])

        # Assert
        assert "There are no inactive sequences to delete. To remove active sequences " + \
               "as well, you need to include an additional flag. Check the client help " + \
               "documentation for more information." in result.output
    
    def test_purge__given_associated_sample_is_still_active_and_force_flag_is_not_present__expect_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'
        shared_group = f'sg-{_new_identifier(10)}'
        proforma_name = f'{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_field_if_not_exists(self.cli, owner_group_field_name)
        _create_field_if_not_exists(self.cli, shared_groups_field_name)
        _create_min_proforma(self.cli, proforma_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        _upload_min_metadata(
            self.cli,
            proforma_name,
            [seq_id, seq_id2],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path)

        # Act
        result = self.cli.invoke([
            'seq',
            'purge',
            '-s',
            seq_id,
            '--delete-all',
            '-t',
            'fasta-cns',
        ])

        # Assert
        assert "Sample is still active." in str(result)

    
    def test_purge__given_associated_sample_is_still_active_and_sequence_is_active_and_delete_all_and_force_flags_are_present__expect_sequence_is_purged(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'
        shared_group = f'sg-{_new_identifier(10)}'
        proforma_name = f'{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_field_if_not_exists(self.cli, owner_group_field_name)
        _create_field_if_not_exists(self.cli, shared_groups_field_name)
        _create_min_proforma(self.cli, proforma_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        _upload_min_metadata(
            self.cli,
            proforma_name,
            [seq_id, seq_id2],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path)
        pre_purge_list = _list_seq_by_group(self.cli, shared_group)
        assert sum(1 for entry in pre_purge_list if entry.get('sampleName') == seq_id) == 1, pre_purge_list
        assert sum(1 for entry in pre_purge_list if entry.get('sampleName') == seq_id2) == 1, pre_purge_list

        # Act
        result = self.cli.invoke([
            'seq',
            'purge',
            '-s',
            seq_id,
            '--delete-all',
            '--force',
            '-t',
            'fasta-cns',
        ])
        
        # Assert
        assert result.exit_code == 0, f'The seq purge command should succeed: {result.output}'
        # _upload_fasta_cns_file(self.cli, cns_fasta_path)
        pre_purge_list2 = _list_seq_by_group(self.cli, shared_group)
        assert sum(1 for entry in pre_purge_list2 if entry.get('sampleName') == seq_id) == 0, pre_purge_list2
        assert sum(1 for entry in pre_purge_list2 if entry.get('sampleName') == seq_id2) == 1, pre_purge_list2
    
    def test_purge__given_sample_has_sequences_but_not_of_the_type_in_the_purge_request__expect_warning_and_no_action(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'
        shared_group = f'sg-{_new_identifier(10)}'
        proforma_name = f'{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_field_if_not_exists(self.cli, owner_group_field_name)
        _create_field_if_not_exists(self.cli, shared_groups_field_name)
        _create_min_proforma(self.cli, proforma_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        _upload_min_metadata(
            self.cli,
            proforma_name,
            [seq_id, seq_id2],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path)

        # Act
        result = self.cli.invoke([
            'seq',
            'purge',
            '-s',
            seq_id,
            '--delete-all',
            '--force',
            '-t',
            'fastq-ill-pe',
        ])
        
        # Assert
        assert "there were no sequences of type $fastq-ill-pe to delete." in result.output
    
    def test_purge__given_sample_has_sequences_of_the_type_in_the_purge_request__expect_sequence_is_purged(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'
        shared_group = f'sg-{_new_identifier(10)}'
        proforma_name = f'{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_field_if_not_exists(self.cli, owner_group_field_name)
        _create_field_if_not_exists(self.cli, shared_groups_field_name)
        _create_min_proforma(self.cli, proforma_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        _upload_min_metadata(
            self.cli,
            proforma_name,
            [seq_id, seq_id2],
            owner_group,
            [shared_group])

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path)
        pre_purge_list = _list_seq_by_group(self.cli, shared_group)
        assert sum(1 for entry in pre_purge_list if entry.get('sampleName') == seq_id) == 1, pre_purge_list
        assert sum(1 for entry in pre_purge_list if entry.get('sampleName') == seq_id2) == 1, pre_purge_list

        # Act
        result = self.cli.invoke([
            'seq',
            'purge',
            '-s',
            seq_id,
            '--delete-all',
            '--force',
            '-t',
            'fasta-cns',
        ])

        # Assert
        assert result.exit_code == 0, f'The seq purge command should succeed: {result.output}'
        # _upload_fasta_cns_file(self.cli, cns_fasta_path)
        pre_purge_list2 = _list_seq_by_group(self.cli, shared_group)
        assert sum(1 for entry in pre_purge_list2 if entry.get('sampleName') == seq_id) == 0, pre_purge_list2
        assert sum(1 for entry in pre_purge_list2 if entry.get('sampleName') == seq_id2) == 1, pre_purge_list2