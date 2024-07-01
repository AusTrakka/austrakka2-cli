from click.testing import CliRunner
from test_utils import _new_identifier


class TestSeqSyncGetCommands:
    runner = CliRunner()

    def test_sync_migrate__given_existing_fasta__expect_migration_to_fasta_cns_with_correct_files_and_contents(self):
        raise NotImplementedError

    def test_sync_migrate__given_existing_fastq__expect_migration_to_fastq_ill_pe_with_correct_files_and_contents(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_no_sequences__expect_no_sequence_downloaded(self):
        raise NotImplementedError

    # parametrize for each sequence type
    def test_sync_get__given_group_has_removed_fasta_cns_sequences__expect_fasta_cns_moved_to_trash_and_other_sequences_unchanged(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_no_sequences__expect_current_state_is__up_to_date(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_no_sequences__expect_current_action_is__pulling_manifest(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_sequences__expect_correct_state_file_name_and_contents(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_sequences_untransformed_during_upload_and_download_was_successful__expect_hashes_of_downloads_to_match_original(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_fasta_asm_sequences_and_download_was_successful__expect_hashes_of_downloads_to_match_transformed_uploads(self):
        raise NotImplementedError
    
    def test_sync_get__given_group_has_fasta_asm_sequences_and_download_was_successful__expect_contigs_are_renamed(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_sequences_and_download_was_successful__expect_sequences_are_listed_in_manifest(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_sequences_and_download_was_successful__expect_current_state_is__up_to_date(self):
        raise NotImplementedError

    def test_sync_get__given_group_has_sequences_and_download_was_successful__expect_current_action_is__pulling_manifest(self):
        raise NotImplementedError
    
    def test_sync_get__given_successful_successive_download_of_multiple_sequence_types__expect_multiple_manifest_and_state_files_and_correct_directory_structure(self):
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
    
    def test_sync_get__given_output_dir_contains_state_file_for_GroupA_and_sync_get_is_run_for_GroupB__expect_command_is_refused(self):
        raise NotImplementedError