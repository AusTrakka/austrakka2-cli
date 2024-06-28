from click.testing import CliRunner
from test_utils import _new_identifier


class TestSeqSyncGetCommands:
    runner = CliRunner()

    def test_sync_get__given_group_has_no_sequences__expect_no_sequence_downloaded(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_no_sequences__expect_current_state_is__up_to_date(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_no_sequences__expect_current_action_is__pulling_manifest(self):
        raise NotImplementedError
