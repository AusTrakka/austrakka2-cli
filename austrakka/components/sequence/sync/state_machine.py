import os
import json

from .constant import *
from .errors import StateMachineError


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


class StateMachine:
    def __init__(self, states: dict[str, State], handlers: dict):
        self.action_handlers = handlers
        self.states: dict[str, State] = states
        self.actions: set[str] = set(handlers.keys())

    def run(self, sync_state: dict):
        if sync_state[CURRENT_STATE_KEY] not in self.states.keys():
            raise StateMachineError(f'The supplied current state '
                                    f'"{sync_state[CURRENT_STATE_KEY]}" is '
                                    f'unknown to this state machine instance.')

        action = sync_state[CURRENT_ACTION_KEY]
        if action is None or action.isspace():
            raise StateMachineError(
                "Cannot set state. The current action is invalid. "
                "Accept only None or non-whitespace-only values.")

        if action not in self.actions:
            raise StateMachineError("The action is unknown to this state machine instance.")

        active_sync_state = sync_state.copy()
        current_state = self.states[active_sync_state[CURRENT_STATE_KEY]]

        while not current_state.is_end_state:
            self.action_handlers[action](active_sync_state)

            # Expect action_handler call to have moved the current
            # state at the end of the call by mutation.
            next_state = active_sync_state[CURRENT_STATE_KEY]
            self._ensure_is_known_state(
                next_state,
                f'The proposed next state is not a known state: "{next_state}". '
                f'Aborting. The unknown state has to be added to the list of '
                f'allowed states.'
            )

            path = os.path.join(
                active_sync_state[OUTPUT_DIR_KEY],
                active_sync_state[SYNC_STATE_FILE_KEY],
            )
            with open(path, 'w') as f:
                json.dump(active_sync_state, f)
                f.close()

            current_state = self.states[active_sync_state[CURRENT_STATE_KEY]]
            action = active_sync_state[CURRENT_ACTION_KEY]

    def get_state(self, name: str) -> State:
        return None if name not in self.states else self.states[name]

    def _ensure_is_known_state(self, name: str, msg: str):
        if name not in self.states:
            raise StateMachineError(msg)
