import pytest

from ete_cmd_bricks import (
    _create_min_proforma_if_not_exists,
    _create_org,
    _create_group,
    _list_seq_by_group,
    _upload_fasta_asm_file, _upload_min_metadata)

from ete_utils import _new_identifier
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

        _create_org(self.cli, org_name)

        # Act
        output = _upload_fasta_asm_file(self.cli, 'test/test-assets/sequences/asm/XYZ-asm-004.fasta', seq_id, org_name)
        print(output)

        # Assert
        result = _list_seq_by_group(self.cli, owner_group)
        assert len(result) == 1, f'Failed to upload fasta asm file: {result}'
