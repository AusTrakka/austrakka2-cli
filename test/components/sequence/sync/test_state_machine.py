import os.path
import json
import pandas as pd
import shutil

from austrakka.components.sequence.sync.state_machine import analyse
from austrakka.components.sequence.sync.state_machine import finalise
from austrakka.components.sequence.sync.state_machine import SName
from austrakka.components.sequence.sync.constant import *


class TestStateMachine:

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
        os.remove(clone)

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
        os.remove(clone)

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
        os.remove(clone)

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
        os.remove(clone)

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
        os.remove(clone)

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
        os.remove(clone)

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
        os.remove(clone)
        os.remove(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY]))
        os.remove(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

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
        path = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        os.remove(clone)
        os.remove(path)
        m = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY])
        os.remove(m)

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

        # Clean up
        os.remove(clone)
        os.remove(path)
        os.remove(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY]))
        oof = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        if os.path.exists(oof):
            os.remove(oof)

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

        # Clean up
        os.remove(clone)
        os.remove(path)
        if os.path.exists(b):
            os.remove(b)
        os.remove(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY]))
        oof = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY])
        if os.path.exists(oof):
            os.remove(oof)

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
        os.remove(clone)
        os.remove(m_path)
        os.remove(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

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
        os.remove(clone)
        os.remove(m_path)
        os.remove(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

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
        os.remove(clone)
        os.remove(m_path)
        os.remove(os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[OBSOLETE_OBJECTS_FILE_KEY]))

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
        r = dt2.loc[(dt2[FILE_PATH_KEY].str.endswith(FASTQ))]
        assert len(r.index) == 0

        # Clean up
        os.remove(clone)
        os.remove(b)
        m = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY])
        os.remove(m)

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
        print(r)
        assert len(r.index) == 1

        # Clean up
        os.remove(clone)
        os.remove(b)
        m = os.path.join(sync_state[OUTPUT_DIR_KEY], sync_state[MANIFEST_KEY])
        os.remove(m)


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
