import pytest

from ete_cmd_bricks import (
    _create_field_if_not_exists,
    _create_min_proforma,
    _create_org,
    _create_group,
    _list_seq_by_group,
    _upload_fasta_asm_file, _upload_min_metadata)

from ete_utils import (
    _new_identifier,
    owner_group_field_name,
    shared_groups_field_name)
from test.utils.austrakka_test_cli import AusTrakkaTestCli

class TestSeqAddCommands:
    @pytest.fixture(autouse=True)
    def _use_cli(self, austrakka_test_cli: AusTrakkaTestCli):
        self.cli = austrakka_test_cli


    def test_seq_add_fasta_asm__given_sample_has_no_prior_asm_sequences__expect_success_without_needing_skip_or_force(self):
        # Arrange
        org_name = f'org-{_new_identifier(4)}'
        seq_id = f'seq-{_new_identifier(10)}'
        owner_group = f'{org_name}-Owner'
        shared_group = f'sg-{_new_identifier(10)}'
        proforma_name = f'{_new_identifier(10)}'

        _create_field_if_not_exists(self.cli, owner_group_field_name)
        _create_field_if_not_exists(self.cli, shared_groups_field_name)
        _create_min_proforma(self.cli, proforma_name)
        _create_org(self.cli, org_name)
        _create_group(self.cli, shared_group)

        _upload_min_metadata(
            self.cli,
            proforma_name,
            [seq_id],
            owner_group,
            [shared_group])

        # Act
        _upload_fasta_asm_file(self.cli, 'test/test-assets/sequences/asm/XYZ-asm-004.fasta', seq_id)

        # Assert
        result = _list_seq_by_group(self.cli, shared_group)
        assert len(result) == 1, f'Failed to add fasta asm file to sequence: {result}'
