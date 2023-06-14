import os
import json
import hashlib
import pandas as pd
from loguru import logger

from ..funcs import _get_seq_data
from austrakka.utils.enums.seq import READ_BOTH
from austrakka.utils.enums.seq import BY_IS_ACTIVE_FLAG
from austrakka.components.sequence.funcs import _download_seq_file
from austrakka.components.sequence.funcs import _get_seq_download_path
from austrakka.utils.retry import retry


class SName:
    PULLING_MANIFEST = 'PULLING_MANIFEST'
    DONE_PULLING_MANIFEST = 'DONE_PULLING_MANIFEST'
    ANALYSING = 'ANALYSING'
    DONE_ANALYSING = 'DONE_ANALYSING'
    DOWNLOADING = 'DOWNLOADING'
    DONE_DOWNLOADING = 'DONE_DOWNLOADING'
    FINALISING = 'FINALISING'
    DONE_FINALISING = 'DONE_FINALISING'
    FINALISATION_FAILED = 'FINALISATION_FAILED'
    PURGING = 'PURGING'
    DONE_PURGING = 'DONE_PURGING'
    UP_TO_DATE = 'UP_TO_DATE'


class Action:
    set_state_pulling_manifest = 'set-state/pulling-manifest'
    pull_manifest = 'pull-manifest'
    set_state_analysing = 'set-state/analysing'
    analyse = 'analyse'
    set_state_downloading = 'set-state/downloading'
    download = 'download'
    set_state_finalising = 'set-state/finalising'
    finalise = 'finalise'
    set_state_purging = 'set-state/purging'
    purge = 'purge'
    set_state_up_to_date = 'set-state/up-to-date'


class State:
    def __init__(
            self,
            name: str,
            is_end_state: bool = False,
            is_start_state: bool = False):

        self.name = name
        self.is_start_state = is_start_state
        self.is_end_state = is_end_state

    def is_valid(self):
        return self and self.name and not self.name.isspace()


class StateGraphError(Exception):
    pass


class StateMachineError(Exception):
    pass


class StateMachine:
    def __init__(self, states: dict[str, State], handlers: dict):
        self.action_handlers = handlers
        self.states: dict[str, State] = states
        self.actions: set[str] = set(handlers.keys())

    def run(self, sync_state: dict):
        if sync_state['current_state'] not in self.states.keys():
            raise StateMachineError('The supplied current state is unknown '
                                    'to this state machine instance.')

        action = sync_state['current_action']
        if action is None or action.isspace():
            raise StateMachineError(
                "Cannot set state. The current action is invalid. "
                "Accept only None or non-whitespace-only values.")

        if action not in self.actions:
            raise StateMachineError("The action is unknown to this state machine instance.")

        active_sync_state = sync_state.copy()
        current_state = self.states[active_sync_state['current_state']]

        while not current_state.is_end_state:
            print("looped")
            self.action_handlers[action](active_sync_state)
            print(f'next_state_name: {active_sync_state["current_state"]}')

            path = os.path.join(
                active_sync_state['output_dir'],
                active_sync_state['sync_state_file'],
            )
            with open(path, 'w') as f:
                json.dump(active_sync_state, f)
                f.close()

            current_state = self.states[active_sync_state['current_state']]
            action = active_sync_state['current_action']

    def get_state(self, name: str) -> State:
        return self.states[name]

    def is_known_state(self, name: str):
        return self.get_state(name) is not None

    def _ensure_is_known_state(self, s: State, msg: str):
        if not self.is_known_state(s.name):
            raise StateMachineError(msg)


def build_state_machine() -> StateMachine:
    return StateMachine({
            SName.PULLING_MANIFEST: State(SName.PULLING_MANIFEST),
            SName.DONE_PULLING_MANIFEST: State(SName.DONE_PULLING_MANIFEST),
            SName.ANALYSING: State(SName.ANALYSING),
            SName.DONE_ANALYSING: State(SName.DONE_ANALYSING),
            SName.DOWNLOADING: State(SName.DOWNLOADING),
            SName.DONE_DOWNLOADING: State(SName.DONE_DOWNLOADING),
            SName.FINALISING: State(SName.FINALISING),
            SName.DONE_FINALISING: State(SName.DONE_FINALISING),
            SName.FINALISATION_FAILED: State(SName.FINALISATION_FAILED, is_end_state=True),
            SName.PURGING: State(SName.PURGING),
            SName.DONE_PURGING: State(SName.DONE_PURGING),
            SName.UP_TO_DATE: State(SName.UP_TO_DATE, is_end_state=True),
        }, {
        Action.set_state_pulling_manifest: _set_state_pulling_manifest,
        Action.pull_manifest: _pull_manifest,
        Action.set_state_analysing: _set_state_analysing,
        Action.analyse: _analyse,
        Action.set_state_downloading: _set_state_downloading,
        Action.download: _download,
        Action.set_state_finalising: _set_state_finalising,
        Action.finalise: _finalise,
        Action.set_state_purging: _set_state_purging,
        Action.purge: _purge,
        Action.set_state_up_to_date: _set_state_up_to_date
        }
    )


def _set_state_pulling_manifest(sync_state: dict):
    print(Action.set_state_pulling_manifest)
    sync_state['current_state'] = SName.PULLING_MANIFEST
    sync_state['current_action'] = Action.pull_manifest


def _pull_manifest(sync_state: dict):
    print(Action.pull_manifest)
    data = _get_seq_data(
        sync_state['seq_type'],
        READ_BOTH,
        sync_state["group_name"],
        BY_IS_ACTIVE_FLAG,
    )

    path = get_path_from_state(sync_state, 'intermediate_manifest_file')
    with open(path, 'w') as f:
        pd.DataFrame(data).to_csv(f, index=False)

    sync_state['current_state'] = SName.DONE_PULLING_MANIFEST
    sync_state['current_action'] = Action.set_state_analysing


def _set_state_analysing(sync_state: dict):
    print(Action.set_state_analysing)
    sync_state['current_state'] = SName.ANALYSING
    sync_state['current_action'] = Action.analyse


def _analyse(sync_state: dict):
    print(Action.analyse)
    df = read_from_csv(sync_state, 'intermediate_manifest_file')

    if 'status' not in df.columns:
        df['status'] = ""

    for index, row in df.iterrows():
        seq_path = os.path.join(
            sync_state["output_dir"],
            str(row["sampleName"]),
            str(row["fileNameOnDisk"]))

        print(seq_path)
        if not os.path.exists(seq_path):
            df.at[index, 'status'] = 'new'
        else:
            file = open(seq_path, 'rb')
            seq_hash = hashlib.sha256(file.read()).hexdigest().lower()
            print(f'local hash:{seq_hash}')
            print(f'server hash: {row["serverSha256"].lower()}')
            if seq_hash == row['serverSha256'].lower():
                df.at[index, 'status'] = 'match'
            else:
                df.at[index, 'status'] = 'drifted'

            file.close()

    save_int_manifest(df, sync_state)
    sync_state['current_state'] = SName.DONE_ANALYSING
    sync_state['current_action'] = Action.set_state_downloading


def _set_state_downloading(sync_state: dict):
    print(Action.set_state_downloading)
    sync_state['current_state'] = SName.DOWNLOADING
    sync_state['current_action'] = Action.download


def _download(sync_state: dict):
    print(Action.download)
    df = read_from_csv(sync_state, 'intermediate_manifest_file')

    if 'hot_swap_name' not in df.columns:
        df["hot_swap_name"] = ""

    save_int_manifest(df, sync_state)

    path = get_path_from_state(sync_state, 'intermediate_manifest_file')
    with open(path, 'w') as f:
        for index, row in df.iterrows():
            if row['status'] != 'downloaded' and row['status'] != 'match':
                try:
                    filename = row['fileNameOnDisk']
                    sample_name = row['sampleName']
                    read = str(row['read'])
                    seq_type = row['type']
                    sample_dir = os.path.join(sync_state['output_dir'], sample_name)
                    file_path = os.path.join(sample_dir, filename)

                    query_path = _get_seq_download_path(
                        sample_name,
                        read,
                        seq_type,
                        BY_IS_ACTIVE_FLAG)

                    if row['status'] == 'drifted':
                        logger.warning(f'Drifted from server: {file_path}. Fixing..')
                        fresh_name = f'{row["fileNameOnDisk"]}.fresh'
                        df.at[index, 'hot_swap_name'] = fresh_name
                        file_path = os.path.join(sample_dir, fresh_name)

                    retry(lambda fp=file_path, fn=filename, qp=query_path, sd=sample_dir:
                          _download_seq_file(file_path, filename, query_path, sample_dir),
                          3,
                          query_path)

                    df.at[index, 'status'] = 'downloaded'
                except Exception as ex:
                    df.at[index, 'status'] = 'failed'
                    logger.error(f'Failed to download: {file_path}. Error: {ex}')

            df.to_csv(f, index=False)
            f.seek(0)
        f.close()

    sync_state['current_state'] = SName.DONE_DOWNLOADING
    sync_state['current_action'] = Action.set_state_finalising


def _set_state_finalising(sync_state: dict):
    print(Action.set_state_finalising)
    sync_state['current_state'] = SName.FINALISING
    sync_state['current_action'] = Action.finalise


def _finalise(sync_state: dict):
    print(Action.finalise)
    df = read_from_csv(sync_state, 'intermediate_manifest_file')
    errors = df.loc[(df["status"] != 'match') & (df['status'] != 'downloaded')]

    if len(errors.index):
        sync_state['current_state'] = SName.FINALISATION_FAILED
        sync_state['current_action'] = Action.set_state_purging
    else:
        files_on_disk = []
        obsoletes = pd.DataFrame({"file_path": []})
        for (root_dir, dir_names, file_names) in os.walk(sync_state["output_dir"]):
            for f in file_names:
                files_on_disk.append((os.path.join(root_dir, f), f))

        for tup in files_on_disk:
            r = df.loc[(df['fileNameOnDisk'] == tup[-1])]
            if len(r.index) == 0:
                obsoletes.loc[len(df)] = tup[1]

        p = get_path_from_state(sync_state, "obsolete_objects_file")
        save_to_csv(obsoletes, p)

        sync_state['current_state'] = SName.DONE_FINALISING
        sync_state['current_action'] = Action.set_state_analysing


def _set_state_purging(sync_state: dict):
    print(Action.set_state_purging)
    sync_state['current_state'] = SName.PURGING
    sync_state['current_action'] = Action.purge


def _purge(sync_state: dict):
    print(Action.purge)
    sync_state['current_state'] = SName.DONE_PURGING
    sync_state['current_action'] = Action.set_state_up_to_date


def _set_state_up_to_date(sync_state: dict):
    print(Action.set_state_up_to_date)
    sync_state['current_state'] = SName.UP_TO_DATE
    sync_state['current_action'] = Action.set_state_pulling_manifest


def get_path_from_state(sync_state: dict, key_to_file: str):
    path = os.path.join(
        sync_state['output_dir'],
        sync_state[key_to_file],
    )
    return path


def read_from_csv(sync_state: dict, state_key: str):
    path = get_path_from_state(sync_state, state_key)
    df = pd.read_csv(path)
    return df


def save_int_manifest(df, sync_state):
    path = get_path_from_state(sync_state, 'intermediate_manifest_file')
    with open(path, 'w') as f:
        df.to_csv(f, index=False)
        f.close()


def save_to_csv(df, path):
    with open(path, 'w') as f:
        df.to_csv(f, index=False)
        f.close()
