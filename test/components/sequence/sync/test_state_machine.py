import os.path
import json
import pandas as pd
import pytest
import shutil
from austrakka.components.sequence.sync.state_machine import _analyse
from austrakka.components.sequence.sync.state_machine import _finalise
from austrakka.components.sequence.sync.state_machine import SName


class TestStateMachine:

    def test_analyse1_new_manifest_entries_expect_entries_marked_as_new(self):
        # Arrange
        sync_state = {
            "sync_state_file": "test-analyse1-sync-state.json",
            "intermediate_manifest_file": "test-analyse1-int-manifest-clone.csv",
            "output_dir": "test/components/sequence/sync/test-assets",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state["output_dir"], "test-analyse1-int-manifest-original.csv")
        clone = os.path.join(sync_state["output_dir"], "test-analyse1-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert 'status' not in df.columns

        # Act
        _analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, ['status']][0]
        assert status == 'new'

        os.remove(clone)

    def test_analyse2_new_manifest_hash_dont_match_local_expect_entries_marked_as_drifted(self):
        # Arrange
        sync_state = {
            "sync_state_file": "test-analyse2-sync-state.json",
            "intermediate_manifest_file": "test-analyse2-int-manifest-clone.csv",
            "output_dir": "test/components/sequence/sync/test-assets",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state["output_dir"], "test-analyse2-int-manifest-original.csv")
        clone = os.path.join(sync_state["output_dir"], "test-analyse2-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert 'status' not in df.columns

        # Act
        _analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, ['status']][0]
        assert status == 'drifted'

        os.remove(clone)

    def test_analyse3_new_manifest_hash_matches_local_expect_entries_marked_as_match(self):
        # Arrange
        sync_state = {
            "sync_state_file": "test-analyse3-sync-state.json",
            "intermediate_manifest_file": "test-analyse3-int-manifest-clone.csv",
            "output_dir": "test/components/sequence/sync/test-assets",
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state["output_dir"], "test-analyse3-int-manifest-original.csv")
        clone = os.path.join(sync_state["output_dir"], "test-analyse3-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert 'status' not in df.columns

        # Act
        _analyse(sync_state)

        # Assert
        df2 = pd.read_csv(clone)
        status = df2.loc[0, ['status']][0]
        assert status == 'match'

        os.remove(clone)

    def test_finalise1_int_manifest_has_failures_expect_finalisation_failed_state(self):
        # Arrange
        sync_state = {
            "sync_state_file": "test-finalisation1-sync-state.json",
            "intermediate_manifest_file": "test-finalise1-int-manifest-clone.csv",
            "output_dir": "test/components/sequence/sync/test-assets",
            "obsolete_objects_file": "test-finalise1-delete-targets.csv"
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state["output_dir"], "test-finalise1-int-manifest-original.csv")
        clone = os.path.join(sync_state["output_dir"], "test-finalise1-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert 'status' in df.columns

        # Act
        _finalise(sync_state)

        # Assert
        assert sync_state['current_state'] == SName.FINALISATION_FAILED

        os.remove(clone)

    def test_finalise2_int_manifest_has_only_downloaded_state_expect_done_finalising_state(self):
        # Arrange
        sync_state = {
            "sync_state_file": "test-finalisation2-sync-state.json",
            "intermediate_manifest_file": "test-finalise2-int-manifest-clone.csv",
            "output_dir": "test/components/sequence/sync/test-assets",
            "obsolete_objects_file": "test-finalise2-delete-targets.csv"
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state["output_dir"], "test-finalise2-int-manifest-original.csv")
        clone = os.path.join(sync_state["output_dir"], "test-finalise2-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert 'status' in df.columns

        # Act
        _finalise(sync_state)

        # Assert
        assert sync_state['current_state'] == SName.DONE_FINALISING

        os.remove(clone)

    def test_finalise3_int_manifest_has_only_match_state_expect_done_finalising_state(self):
        # Arrange
        sync_state = {
            "sync_state_file": "test-finalisation3-sync-state.json",
            "intermediate_manifest_file": "test-finalise3-int-manifest-clone.csv",
            "output_dir": "test/components/sequence/sync/test-assets",
            "obsolete_objects_file": "test-finalise3-delete-targets.csv"
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state["output_dir"], "test-finalise3-int-manifest-original.csv")
        clone = os.path.join(sync_state["output_dir"], "test-finalise3-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert 'status' in df.columns

        # Act
        _finalise(sync_state)

        # Assert
        assert sync_state['current_state'] == SName.DONE_FINALISING

        os.remove(clone)

    def test_finalise4_files_on_disk_not_in_int_manifest_expect_added_to_delete_target(self):
        # Arrange
        sync_state = {
            "sync_state_file": "test-finalise4-sync-state.json",
            "intermediate_manifest_file": "test-finalise4-int-manifest-clone.csv",
            "output_dir": "test/components/sequence/sync/finalise4",
            "obsolete_objects_file": "test-finalise4-delete-targets.csv"
        }

        # make a clone of the original test manifest because the test subject will
        # be mutating it. The clone must be deleted by the test afterwards.
        original = os.path.join(sync_state["output_dir"], "test-finalise4-int-manifest-original.csv")
        clone = os.path.join(sync_state["output_dir"], "test-finalise4-int-manifest-clone.csv")
        shutil.copy(original, clone)

        # Check that the test data start out clean
        df = pd.read_csv(clone)
        assert 'status' in df.columns

        # Act
        _finalise(sync_state)

        # Assert
        assert sync_state['current_state'] == SName.DONE_FINALISING

        # Sample60 is the extra
        df = read_from_csv(sync_state, 'obsolete_objects_file')
        r = df.loc[(df["file_path"].str.endswith("Sample60_20230614T00453848_a34d8705_R1.fastq"))]
        assert len(r.index) == 1

        os.remove(clone)


def read_from_csv(sync_state: dict, state_key: str):
    path = os.path.join(
        sync_state['output_dir'],
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
