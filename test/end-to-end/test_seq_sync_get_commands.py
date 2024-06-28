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

    def test_sync_get__given_group_has_sequences_and_download_was_successful__expect_hashes_of_downloads_to_match_original(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_sequences_and_download_was_successful__expect_sequences_are_listed_in_manifest(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_sequences_and_download_was_successful__expect_current_state_is__up_to_date(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_sequences_and_download_was_successful__expect_current_action_is__pulling_manifest(self):
        raise NotImplementedError

    def test_sync_get__given_output_dir_was_used_for_group_A_and_now_used_for_group_B__expect_command_is_refused(self):
        raise NotImplementedError

    def test_sync_get__given_previous_successful_download_and_local_file_is_deleted__expect_file_is_repaired(self):
        raise NotImplementedError

    def test_sync_get__given_previous_successful_download_and_local_file_is_altered__expect_file_is_repaired(self):
        raise NotImplementedError

    def test_sync_get__given_previous_successful_download_and_sample_is_removed_from_group__expect_local_file_is_moved_to_trash(self):
        raise NotImplementedError

    def test_sync_get__given_stray_files_were_added_to_output_directory_and_the_next_run_is_successful__expect_stray_files_are_moved_to_trash(self):
        raise NotImplementedError