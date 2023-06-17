import os.path
import json
import pandas as pd
import shutil

from datetime import datetime

from austrakka.components.sequence.sync.sync_workflow import analyse
from austrakka.components.sequence.sync.sync_workflow import finalise
from austrakka.components.sequence.sync.sync_workflow import purge
from austrakka.components.sequence.sync.state_machine import SName
from austrakka.components.sequence.sync.state_machine import Action
from austrakka.components.sequence.sync.constant import *


class TestSyncWorkflow:

    def test_analyse1_new_manifest_entries_expect_entries_marked_as_new(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-analyse1-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-analyse1-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/test-assets",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse1-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse1-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY not in df.columns

        # Act
        analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, [STATUS_KEY]][0]
        assert status == MISSING

        # Clean up
        clean_up_path(clone)

    def test_analyse2_new_manifest_hash_dont_match_local_expect_entries_marked_as_drifted(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-analyse2-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-analyse2-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/test-assets",
            HASH_CHECK_KEY: True,
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse2-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse2-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY not in df.columns

        # Act
        analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, [STATUS_KEY]][0]
        assert status == DRIFTED

        # Clean up
        clean_up_path(clone)

    def test_analyse3_new_manifest_hash_matches_local_expect_entries_marked_as_match(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-analyse3-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-analyse3-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/test-assets",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse3-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse3-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY not in df.columns

        # Act
        analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, [STATUS_KEY]][0]
        assert status == MATCH

        # Clean up
        clean_up_path(clone)

    def test_analyse4_given_skip_hash_check_option_expect_comparison_by_file_name_only(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-analyse4-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-analyse4-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/analyse4",
            HASH_CHECK_KEY: False
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse4-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse4-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY not in df.columns

        # Act
        analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, [STATUS_KEY]][0]
        assert status == MATCH

        # Clean up
        clean_up_path(clone)

    def test_analyse5_hash_check_option_omitted_expect_hash_check_is_on_by_default(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-analyse5-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-analyse5-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/test-assets",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse5-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse5-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY not in df.columns

        # Act
        analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, [STATUS_KEY]][0]
        assert status == DRIFTED

        # Clean up
        clean_up_path(clone)

    def test_analyse6_restarting_analyse_expect_no_hash_check_for_entries_already_matched(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-analyse6-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-analyse6-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/analyse6",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse6-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse6-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # This is a restart analysis test. There should already be a status key
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, [STATUS_KEY]][0]
        assert status == MATCH

        # Clean up
        clean_up_path(clone)

    # Failure at the download stage. The file started partial download
    # and then encountered an exception. The failure is picked up at
    # the finalise stage.
    def test_analyse7_when_resuming_from_finalise_failed_partial_download_expect_failed_file_marked_as_drifted(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-analyse7-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-analyse7-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/analyse7",
            CURRENT_STATE_KEY: SName.FINALISATION_FAILED,
            CURRENT_ACTION_KEY: Action.analyse,
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse7-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse7-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # This is a restart analysis test. There should already be a status key
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, [STATUS_KEY]][0]
        assert status == DRIFTED

        # Clean up
        clean_up_path(clone)

    # Failure at the download stage. The file download did not start
    # and then encountered an exception. The failure is picked up at
    # the finalise stage.
    def test_analyse8_when_resuming_from_finalise_failed_no_download_expect_failed_file_marked_as_missing(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-analyse8-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-analyse8-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/analyse8",
            CURRENT_STATE_KEY: SName.FINALISATION_FAILED,
            CURRENT_ACTION_KEY: Action.analyse,
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse8-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse8-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # This is a restart analysis test. There should already be a status key
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, [STATUS_KEY]][0]
        assert status == MISSING

        # Clean up
        clean_up_path(clone)

    # Failure at the download stage. The file was partially downloaded
    # and then encountered an exception. The failure is picked up at
    # the finalise stage. Expect hash check to be forcefully performed
    # even if the cli options says other wise.
    def test_analyse9_when_resuming_from_finalise_failed_part_download_expect_forced_hash_check(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-analyse9-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-analyse9-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/analyse9",
            CURRENT_STATE_KEY: SName.FINALISATION_FAILED,
            CURRENT_ACTION_KEY: Action.analyse,
            HASH_CHECK_KEY: False
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse9-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-analyse9-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # This is a restart analysis test. There should already be a status key
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, [STATUS_KEY]][0]
        assert status == DRIFTED

        # Clean up
        clean_up_path(clone)

    def test_finalise1_int_manifest_has_failures_expect_finalisation_failed_state(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalisation1-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise1-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/test-assets",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise1-delete-targets.csv",
            MANIFEST_KEY: "test-finalise1-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise1-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise1-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.FINALISATION_FAILED

        # Clean up
        clean_up_path(clone)

    def test_finalise2_int_manifest_has_only_downloaded_state_expect_done_finalising_state(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalisation2-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise2-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/test-assets",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise2-delete-targets.csv",
            MANIFEST_KEY: "test-finalise2-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise2-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise2-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.DONE_FINALISING

        # Clean up
        clean_up_path(clone)
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY]))
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

    def test_finalise3_int_manifest_has_only_match_state_expect_done_finalising_state(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalisation3-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise3-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/test-assets",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise3-delete-targets.csv",
            MANIFEST_KEY: "test-finalise3-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise3-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise3-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.DONE_FINALISING

        # Clean up
        clean_up_path(clone)
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY]))

    def test_finalise4_files_on_disk_not_in_int_manifest_expect_added_to_delete_target(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalise4-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise4-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/finalise4",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise4-delete-targets.csv",
            MANIFEST_KEY: "test-finalise4-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise4-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise4-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        time_stamp_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.DONE_FINALISING

        # Sample60 is the extra
        path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        df = pd.read_csv(path)
        r = df.loc[
            (df[FILE_NAME_KEY] == "Sample60_20230614T00453848_a34d8705_R1.fastq") |
            (df[FILE_NAME_KEY] == "Sample70_20230614T00453848_a34d8705_R1.fastq.gz") |
            (df[FILE_NAME_KEY] == "Sample80_20230614T00453848_a34d8705_R1.fasta") |
            (df[FILE_NAME_KEY] == "Sample90_20230614T00453848_a34d8705_R1.fasta.gz")
        ]
        assert len(r.index) == 4

        # Note! This is a string order comparision and not date time.
        d = df.loc[(df[DETECTION_DATE_KEY] > time_stamp_str)]
        assert len(d.index) == 4

        # Clean up
        clean_up_path(clone)
        clean_up_path(path)
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY]))
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

    def test_finalise5_given_match_status_and_successful_finalise_expect_convert_int_manifest_to_live_manifest(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalise5-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise5-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/finalise5",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise5-delete-targets.csv",
            MANIFEST_KEY: "test-finalise5-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise5-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise5-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.DONE_FINALISING

        m_path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY])
        m_df = pd.read_csv(m_path)

        im_path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])
        im_df = pd.read_csv(im_path)

        assert im_df.at[0, STATUS_KEY] == DONE
        assert im_df.at[0, FILE_NAME_ON_DISK_KEY] == m_df.at[0, FASTQ_R1_KEY]
        assert im_df.at[0, READ_KEY] == 1
        assert im_df.at[0, SAMPLE_NAME_KEY] == 'Sample5'
        assert im_df.at[1, STATUS_KEY] == DONE
        assert im_df.at[1, FILE_NAME_ON_DISK_KEY] == m_df.at[0, FASTQ_R2_KEY]
        assert im_df.at[1, READ_KEY] == 2
        assert im_df.at[1, SAMPLE_NAME_KEY] == 'Sample5'
        assert m_df.at[0, SEQ_ID_KEY] == 'Sample5'

        # Clean up
        clean_up_path(clone)
        clean_up_path(m_path)
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

    def test_finalise6_given_downloaded_status_and_successful_finalise_expect_convert_int_manifest_to_live_manifest(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalise6-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise6-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/finalise6",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise6-delete-targets.csv",
            MANIFEST_KEY: "test-finalise6-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise6-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise6-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.DONE_FINALISING

        m_path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY])
        m_df = pd.read_csv(m_path)

        im_path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])
        im_df = pd.read_csv(im_path)

        assert im_df.at[0, STATUS_KEY] == DONE
        assert im_df.at[0, FILE_NAME_ON_DISK_KEY] == m_df.at[0, FASTQ_R1_KEY]
        assert im_df.at[0, READ_KEY] == 1
        assert im_df.at[0, SAMPLE_NAME_KEY] == 'Sample5'
        assert im_df.at[1, STATUS_KEY] == DONE
        assert im_df.at[1, FILE_NAME_ON_DISK_KEY] == m_df.at[0, FASTQ_R2_KEY]
        assert im_df.at[1, READ_KEY] == 2
        assert im_df.at[1, SAMPLE_NAME_KEY] == 'Sample5'
        assert m_df.at[0, SEQ_ID_KEY] == 'Sample5'

        # Clean up
        clean_up_path(clone)
        clean_up_path(m_path)
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

    def test_finalise7_given_drifted_status_expect_fresh_download_from_previous_step_is_hot_swapped(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalise7-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise7-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/finalise7",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise7-delete-targets.csv",
            MANIFEST_KEY: "test-finalise7-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise7-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise7-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # make a clone of original inputs so that when the files are moved by _finalise()
        # this test can still be re-run.
        a = os.path.join(sync_state[OUTPUT_DIR_KEY],
                         "Sample5/Sample5_20230614T00453848_a34d8705_R1.fastq.fresh.original")
        b = os.path.join(sync_state[OUTPUT_DIR_KEY],
                         "Sample5/Sample5_20230614T00453848_a34d8705_R1.fastq.fresh")
        shutil.copy(a, b)

        c = os.path.join(sync_state[OUTPUT_DIR_KEY],
                         "Sample5/Sample5_20230614T00453848_a34d8705_R1.fastq.original")
        d = os.path.join(sync_state[OUTPUT_DIR_KEY],
                         "Sample5/Sample5_20230614T00453848_a34d8705_R1.fastq")
        shutil.copy(c, d)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Preliminary check of freshly download content
        path_to_fresh = get_file_path(df, sync_state, HOT_SWAP_NAME_KEY)
        assert os.path.exists(path_to_fresh)
        fresh_content = read_content(path_to_fresh)
        assert fresh_content[0] == 'def'

        # Preliminary check of original content which has been deemed to have drifted
        path_to_original = get_file_path(df, sync_state, FILE_NAME_ON_DISK_KEY)
        assert os.path.exists(path_to_original)
        original_content = read_content(path_to_original)
        assert original_content[0] == 'abc'

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.DONE_FINALISING
        assert not os.path.exists(path_to_fresh)
        assert os.path.exists(path_to_original)
        original_content = read_content(path_to_original)
        assert original_content[0] == 'def'

        m_path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY])
        m_df = pd.read_csv(m_path)

        im_path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])
        im_df = pd.read_csv(im_path)

        assert im_df.at[0, STATUS_KEY] == DONE
        assert im_df.at[0, FILE_NAME_ON_DISK_KEY] == m_df.at[0, FASTQ_R1_KEY]
        assert im_df.at[0, READ_KEY] == 1
        assert im_df.at[0, SAMPLE_NAME_KEY] == 'Sample5'
        assert im_df.at[1, STATUS_KEY] == DONE

        # Clean up
        clean_up_path(clone)
        clean_up_path(m_path)
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

    def test_finalise8_file_on_delete_target_is_also_in_int_manifest_expect_removed_from_delete_target(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalise8-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise8-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/finalise8",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise8-delete-targets.csv",
            MANIFEST_KEY: "test-finalise8-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise8-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise8-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # also clone the delete-targets.csv to support re-entrant testing
        a = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise8-delete-targets.csv.original")
        b = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise8-delete-targets.csv")
        shutil.copy(a, b)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # confirm the initial state of test-finalise8-delete-targets.csv
        dt = pd.read_csv(b)
        assert dt.at[0, FILE_PATH_KEY] == 'test/components/sequence/sync/finalise8/' \
                                          'Sample5/Sample5_20230614T00453848_a34d8705_R1.fastq'

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.DONE_FINALISING

        dt2 = pd.read_csv(b)
        # Because it's a test environment with test artifacts, finalise() might pickup
        # strays. We just want to check that there are no fastq files in the list.
        r = dt2.loc[(dt2[FILE_PATH_KEY].str.endswith(FASTQ_EXT))]
        assert len(r.index) == 0

        # Clean up
        clean_up_path(clone)
        clean_up_path(b)
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY]))

    def test_finalise9_given_existing_delete_target_entries_expect_entries_preserved_after_finalisation(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalise9-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise9-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/finalise9",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise9-delete-targets.csv",
            MANIFEST_KEY: "test-finalise9-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise9-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise9-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # also clone the delete-targets.csv to support re-entrant testing
        a = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise9-delete-targets.csv.original")
        b = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise9-delete-targets.csv")
        shutil.copy(a, b)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # confirm the initial state of test-finalise9-delete-targets.csv
        dt = pd.read_csv(b)
        assert dt.at[0, FILE_PATH_KEY] == 'test/components/sequence/sync/finalise9/' \
                                          'Sample5/something-to-be-deleted.fastq'

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.DONE_FINALISING

        dt2 = pd.read_csv(b)
        # Because it's a test environment with test artifacts, finalise() might pickup
        # strays. We just want to check that there are no fastq files in the list.
        r = dt2.loc[(dt2[FILE_NAME_KEY] == "something-to-be-deleted.fastq")]
        assert len(r.index) == 1

        d = dt2.loc[(dt2[DETECTION_DATE_KEY] == "2005-05-05")]
        assert len(d.index) == 1

        # Clean up
        clean_up_path(clone)
        clean_up_path(b)
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY]))

    def test_finalise10_files_already_in_delete_target_expect_to_not_add_duplicates_to_list(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-finalise10-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-finalise10-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/finalise10",
            OBSOLETE_OBJECTS_FILE_KEY: "test-finalise10-delete-targets.csv",
            MANIFEST_KEY: "test-finalise10-manifest.csv",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise10-int-manifest-original.csv")
        clone = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise10-int-manifest-clone.csv")
        shutil.copy(original, clone)

        a = os.path.join(sync_state[OUTPUT_DIR_KEY], "test-finalise10-delete-targets.csv.original")
        b = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        shutil.copy(a, b)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert STATUS_KEY in df.columns

        # Act
        finalise(sync_state)

        # Assert
        assert sync_state[CURRENT_STATE_KEY] == SName.DONE_FINALISING

        # Sample60 is the extra
        path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        df = pd.read_csv(path)
        r = df.loc[(df[FILE_NAME_KEY] == "Sample60_20230614T00453848_a34d8705_R1.fastq")]
        assert len(r.index) == 1
        assert len(df.index) == 1

        # Clean up
        clean_up_path(clone)
        clean_up_path(path)
        clean_up_path(b)
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY]))
        clean_up_path(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

    def test_purge1_file_marked_as_obsolete_and_exists_expect_file_is_deleted(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-purge1-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-purge1-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/purge1",
            OBSOLETE_OBJECTS_FILE_KEY: "test-purge1-delete-targets.csv",
            TRASH_DIR_KEY: ".trash",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        a = os.path.join(
            "test/components/sequence/sync/test-assets",
            "empty-intermediate-manifest-original.csv")
        b = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])
        shutil.copy(a, b)

        c = os.path.join(
            "test/components/sequence/sync/test-assets",
            "purge1-delete-targets.csv.original")
        d = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        shutil.copy(c, d)

        dest_dir = os.path.join(sync_state[OUTPUT_DIR_KEY], "Sample60")
        os.makedirs(dest_dir, exist_ok=True)
        obsolete_fastq = "test/components/sequence/sync/test-assets/a.fastq"
        shutil.copy(obsolete_fastq, dest_dir)

        # Act
        purge(sync_state)

        # Assert
        fastq_final_path = os.path.join(dest_dir, "a.fastq")
        assert not os.path.exists(fastq_final_path)

        # Clean up
        clean_up_dir(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[TRASH_DIR_KEY]))

    def test_purge2_given_empty_sub_dirs_in_output_dir_expect_dir_deleted(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-purge2-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-purge2-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/purge2",
            OBSOLETE_OBJECTS_FILE_KEY: "test-purge2-delete-targets.csv",
            TRASH_DIR_KEY: ".trash",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        a = os.path.join(
            "test/components/sequence/sync/test-assets",
            "empty-intermediate-manifest-original.csv")
        b = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])
        shutil.copy(a, b)

        c = os.path.join(
            "test/components/sequence/sync/test-assets",
            "purge2-delete-targets.csv.original")
        d = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        shutil.copy(c, d)

        dest_dir = os.path.join(sync_state[OUTPUT_DIR_KEY], "Sample60")
        os.makedirs(dest_dir, exist_ok=True)
        obsolete_fastq = "test/components/sequence/sync/test-assets/a.fastq"
        shutil.copy(obsolete_fastq, dest_dir)

        # Act
        purge(sync_state)

        # Assert
        assert not os.path.exists(dest_dir)

        # Clean up
        clean_up_dir(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[TRASH_DIR_KEY]))

    def test_purge3_given_trash_dir_is_empty_expect_dir_ignored(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-purge3-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-purge3-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/purge3",
            OBSOLETE_OBJECTS_FILE_KEY: "test-purge3-delete-targets.csv",
            TRASH_DIR_KEY: ".trash",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        a = os.path.join(
            "test/components/sequence/sync/test-assets",
            "empty-intermediate-manifest-original.csv")
        b = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])
        shutil.copy(a, b)

        c = os.path.join(
            "test/components/sequence/sync/test-assets",
            "purge3-delete-targets.csv.original")
        d = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        shutil.copy(c, d)

        trash_dir = os.path.join(sync_state[OUTPUT_DIR_KEY], TRASH_DIR)
        os.makedirs(trash_dir, exist_ok=True)

        # Act
        purge(sync_state)

        # Assert
        assert os.path.exists(trash_dir)

        # Clean up
        clean_up_dir(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[TRASH_DIR_KEY]))

    def test_purge4_given_file_is_moved_to_trash_expect_same_sub_dir_structures(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-purge4-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-purge4-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/purge4",
            OBSOLETE_OBJECTS_FILE_KEY: "test-purge4-delete-targets.csv",
            TRASH_DIR_KEY: ".trash",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        a = os.path.join(
            "test/components/sequence/sync/test-assets",
            "empty-intermediate-manifest-original.csv")
        b = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])
        shutil.copy(a, b)

        c = os.path.join(
            "test/components/sequence/sync/test-assets",
            "purge4-delete-targets.csv.original")
        d = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        shutil.copy(c, d)

        dest_dir = os.path.join(sync_state[OUTPUT_DIR_KEY], "dir1", "dir2")
        os.makedirs(dest_dir, exist_ok=True)
        obsolete_fastq = "test/components/sequence/sync/test-assets/a.fastq"
        shutil.copy(obsolete_fastq, dest_dir)

        # Act
        purge(sync_state)

        # Assert
        assert os.path.exists(os.path.join(sync_state[OUTPUT_DIR_KEY], TRASH_DIR, "dir1"))
        assert os.path.exists(os.path.join(sync_state[OUTPUT_DIR_KEY], TRASH_DIR, "dir1", "dir2"))
        assert os.path.exists(os.path.join(sync_state[OUTPUT_DIR_KEY], TRASH_DIR, "dir1", "dir2", "a.fastq"))

        # Clean up
        clean_up_dir(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[TRASH_DIR_KEY]))

    def test_purge5_when_successful_expect_obsolete_objects_file_deleted(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-purge5-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-purge5-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/purge5",
            OBSOLETE_OBJECTS_FILE_KEY: "test-purge5-delete-targets.csv",
            TRASH_DIR_KEY: ".trash",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        a = os.path.join(
            "test/components/sequence/sync/test-assets",
            "empty-intermediate-manifest-original.csv")
        b = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])
        shutil.copy(a, b)

        c = os.path.join(
            "test/components/sequence/sync/test-assets",
            "purge5-delete-targets.csv.original")
        delete_target_file = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        shutil.copy(c, delete_target_file)

        # Act
        purge(sync_state)

        # Assert
        assert not os.path.exists(delete_target_file)

        # Clean up
        clean_up_dir(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[TRASH_DIR_KEY]))

    def test_purge6_when_successful_expect_int_manifest_deleted(self):
        # Arrange
        sync_state = {
            SYNC_STATE_FILE_KEY: "test-purge6-sync-state.json",
            INTERMEDIATE_MANIFEST_FILE_KEY: "test-purge6-int-manifest-clone.csv",
            OUTPUT_DIR_KEY: "test/components/sequence/sync/purge6",
            OBSOLETE_OBJECTS_FILE_KEY: "test-purge6-delete-targets.csv",
            TRASH_DIR_KEY: ".trash",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        a = os.path.join(
            "test/components/sequence/sync/test-assets",
            "empty-intermediate-manifest-original.csv")
        int_man = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[INTERMEDIATE_MANIFEST_FILE_KEY])
        shutil.copy(a, int_man)

        c = os.path.join(
            "test/components/sequence/sync/test-assets",
            "purge6-delete-targets.csv.original")
        d = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        shutil.copy(c, d)

        # Act
        purge(sync_state)

        # Assert
        assert not os.path.exists(int_man)

        # Clean up
        clean_up_dir(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[TRASH_DIR_KEY]))


def read_content(path_to_fresh):
    f = open(path_to_fresh, 'r')
    c = f.readlines()
    f.close()
    return c


def get_file_path(df, sync_state, key):
    return os.path.join(
        sync_state[OUTPUT_DIR_KEY],
        df.at[0, SAMPLE_NAME_KEY],
        df.at[0, key]
    )


def read_from_csv(sync_state: dict, state_key: str):
    path = os.path.join(
        sync_state[OUTPUT_DIR_KEY],
        sync_state[state_key],
    )
    df = pd.read_csv(path)
    return df


def read_json(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    else:
        return {}


def clean_up_path(b):
    if os.path.exists(b):
        os.remove(b)


def clean_up_dir(b):
    if os.path.exists(b):
        shutil.rmtree(b)
