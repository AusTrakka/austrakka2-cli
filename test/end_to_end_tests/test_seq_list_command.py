import json
import pytest

from ete_cmd_bricks import (
    _create_field_if_not_exists,
    _create_min_proforma_if_not_exists,
    _create_org,
    _upload_fasta_cns_file,
    _upload_fastq_ill_pe_file, _create_project)

from ete_utils import (
    _new_identifier,
    seq_id_field_name,
    _clone_cns_fasta_file)
from test.utils.austrakka_test_cli import AusTrakkaTestCli


class TestSeqGetCommand:
    @pytest.fixture(autouse=True)
    def _use_cli(self, austrakka_test_cli: AusTrakkaTestCli):
        self.cli = austrakka_test_cli

    
    def test_list__given_group_name_and_seq_id_are_not_specified__expect_cli_error(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_project = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_min_proforma_if_not_exists(self.cli)
        _create_org(self.cli, org_name)
        _create_project(self.cli, shared_project)

        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name, [shared_project])

        # Act
        result = self.cli.invoke([
            'seq',
            'list',
            '-t',
            'fasta-cns',
        ])

        # Assert
        assert result.exit_code != 0, f'The seq get command should fail: {result.output}'
        assert ("You must provide at least one of these arguments: "
                "`group-name, seq-id`.") in result.output



    def test_list__given_type_is_not_specified__expect_all_types_are_listed(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_project = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_min_proforma_if_not_exists(self.cli)
        _create_org(self.cli, org_name)
        _create_project(self.cli, shared_project)

        # Upload fasta
        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name, [shared_project])

        # Upload fastq
        original_file1 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r1.fastq'
        original_file2 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r2.fastq'
        _upload_fastq_ill_pe_file(self.cli, seq_id, original_file1, original_file2, org_name, [shared_project])

        # Act
        result = self.cli.invoke([
            'seq',
            'list',
            '-s',
            seq_id,
            '-f',
            'json'
        ])
        
        # Assert
        assert result.exit_code == 0, f'The seq get command should succeed: {result.output}'
        json_result = json.loads(result.output)

        # Count elements by type
        fastq_ill_pe_count = sum(1 for item in json_result if item.get("type") == "fastq-ill-pe")
        fasta_cns_count = sum(1 for item in json_result if item.get("type") == "fasta-cns")

        # Check if counts match expected values
        assert fastq_ill_pe_count == 2, f"Expected 2 elements with type 'fastq-ill-pe', but found {fastq_ill_pe_count}"
        assert fasta_cns_count == 1, f"Expected 1 element with type 'fasta-cns', but found {fasta_cns_count}"
    
    
    def test_list__given_type_is_specified__expect_only_sequence_of_that_type_listed(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_project = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_min_proforma_if_not_exists(self.cli)
        _create_org(self.cli, org_name)
        _create_project(self.cli, shared_project)

        # Upload fasta
        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name, [shared_project])

        # Upload fastq
        original_file1 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r1.fastq'
        original_file2 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r2.fastq'
        _upload_fastq_ill_pe_file(self.cli, seq_id, original_file1, original_file2, org_name, [shared_project])

        # Act
        result = self.cli.invoke([
            'seq',
            'list',
            '-t',
            'fastq-ill-pe',
            '-s',
            seq_id,
            '-f',
            'json'
        ])

        # Assert
        assert result.exit_code == 0, f'The seq get command should succeed: {result.output}'
        json_result = json.loads(result.output)

        # Count elements by type
        fastq_ill_pe_count = sum(1 for item in json_result if item.get("type") == "fastq-ill-pe")
        fasta_cns_count = sum(1 for item in json_result if item.get("type") == "fasta-cns")

        # Check if counts match expected values
        assert fastq_ill_pe_count == 2, f"Expected 2 elements with type 'fastq-ill-pe', but found {fastq_ill_pe_count}"
        assert fasta_cns_count == 0, f"Expected 0 element with type 'fasta-cns', but found {fasta_cns_count}"
    
    
    def test_list__given_group_name_is_specified__expect_only_sequences_in_that_group_are_listed(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_project = f'sg-{_new_identifier(10)}'
        project_group = f'{shared_project}-Group'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_min_proforma_if_not_exists(self.cli)
        _create_org(self.cli, org_name)
        _create_project(self.cli, shared_project)

        # Upload fasta
        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name, [shared_project])

        # Upload fastq
        original_file1 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r1.fastq'
        original_file2 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r2.fastq'
        _upload_fastq_ill_pe_file(self.cli, seq_id, original_file1, original_file2, org_name, [shared_project])

        # Act
        result = self.cli.invoke([
            'seq',
            'list',
            '-t',
            'fastq-ill-pe',
            '-g',
            project_group,
            '-f',
            'json'
        ])

        # Assert
        assert result.exit_code == 0, f'The seq get command should succeed: {result.output}'
        json_result = json.loads(result.output)

        # Count elements by type
        fastq_ill_pe_count = sum(1 for item in json_result if item.get("type") == "fastq-ill-pe")
        fasta_cns_count = sum(1 for item in json_result if item.get("type") == "fasta-cns")

        # Check if counts match expected values
        assert fastq_ill_pe_count == 2, f"Expected 2 elements with type 'fastq-ill-pe', but found {fastq_ill_pe_count}"
        assert fasta_cns_count == 0, f"Expected 0 element with type 'fasta-cns', but found {fasta_cns_count}"
    
    
    def test_list__given_seq_id_is_specified__expect_only_sequence_for_the_sample_with_that_id_is_listed(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        seq_id2 = f'seq-{_new_identifier(10)}'
        shared_project = f'sg-{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, seq_id_field_name)
        _create_min_proforma_if_not_exists(self.cli)
        _create_org(self.cli, org_name)
        _create_project(self.cli, shared_project)

        # Upload fasta
        original_file = 'test/test-assets/sequences/cns/multi-seq-cns.fasta'
        cns_fasta_path = _clone_cns_fasta_file(
            original_file,
            [('SEQ_multi-seq-cns-001', seq_id), ('SEQ_multi-seq-cns-002', seq_id2)])

        _upload_fasta_cns_file(self.cli, cns_fasta_path, org_name, [shared_project])

        # Upload fastq
        original_file1 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r1.fastq'
        original_file2 = 'test/test-assets/sequences/ill-pe/ill-pe-001_r2.fastq'
        _upload_fastq_ill_pe_file(self.cli, seq_id, original_file1, original_file2, org_name, [shared_project])

        # Act
        result = self.cli.invoke([
            'seq',
            'list',
            '-t',
            'fastq-ill-pe',
            '-s',
            seq_id,
            '-f',
            'json'
        ])

        # Assert
        assert result.exit_code == 0, f'The seq get command should succeed: {result.output}'
        json_result = json.loads(result.output)

        # Count elements by type
        fastq_ill_pe_count = sum(1 for item in json_result if item.get("type") == "fastq-ill-pe")
        fasta_cns_count = sum(1 for item in json_result if item.get("type") == "fasta-cns")

        # Check if counts match expected values
        assert fastq_ill_pe_count == 2, f"Expected 2 elements with type 'fastq-ill-pe', but found {fastq_ill_pe_count}"
        assert fasta_cns_count == 0, f"Expected 0 element with type 'fasta-cns', but found {fasta_cns_count}"
