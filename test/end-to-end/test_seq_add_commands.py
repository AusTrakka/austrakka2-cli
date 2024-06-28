from click.testing import CliRunner
from test_utils import _new_identifier

from test_cmd_bricks import (
    _create_field_if_not_exists,
    _create_min_proforma,
    _create_org,
    _create_group,
    _get_seq_by_group,
    _upload_fasta_asm_file, _upload_min_metadata)

from test_utils import (
    seq_id_field_name,
    owner_group_field_name,
    shared_groups_field_name)


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
