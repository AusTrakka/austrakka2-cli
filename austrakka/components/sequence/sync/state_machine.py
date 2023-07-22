import json

from .constant import CURRENT_STATE_KEY
from .constant import CURRENT_ACTION_KEY
from .constant import SYNC_STATE_FILE_KEY
from .errors import StateMachineError
from .sync_io import get_path


# pylint: disable=too-few-public-methods
class SName:
    PULLING_MANIFEST = 'PULLING_MANIFEST'
    DONE_PULLING_MANIFEST = 'DONE_PULLING_MANIFEST'
    ANALYSING = 'ANALYSING'
    DONE_ANALYSING = 'DONE_ANALYSING'
    DOWNLOADING = 'DOWNLOADING'
    DONE_DOWNLOADING = 'DONE_DOWNLOADING'
    AGGREGATING = 'AGGREGATING'
    DONE_AGGREGATING = 'DONE_AGGREGATING'
    FINALISING = 'FINALISING'
    DONE_FINALISING = 'DONE_FINALISING'
    FINALISATION_FAILED = 'FINALISATION_FAILED'
    PURGING = 'PURGING'
    DONE_PURGING = 'DONE_PURGING'
    UP_TO_DATE = 'UP_TO_DATE'


# pylint: disable=too-few-public-methods
class Action:
    set_state_pulling_manifest = 'set-state/pulling-manifest'
    pull_manifest = 'pull-manifest'
    set_state_analysing = 'set-state/analysing'
    analyse = 'analyse'
    set_state_downloading = 'set-state/downloading'
    download = 'download'
    set_state_aggregating = 'set-state/aggregating'
    aggregate = 'aggregate'
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
        self.ensure_valid_next_state(sync_state[CURRENT_STATE_KEY])
        self.ensure_valid_next_action(sync_state[CURRENT_ACTION_KEY])

        active_sync_state = sync_state.copy()
        current_state = self.states[active_sync_state[CURRENT_STATE_KEY]]

        while not current_state.is_end_state:
            self.action_handlers[
                active_sync_state[CURRENT_ACTION_KEY]
            ](active_sync_state)

            # Expect action_handler call to have moved the current
            # state and action at the end of the call by mutation.
            # So in effect, the next state/action is already set
            # as the current and is just waiting for the next loop.
            # check that both are valid.
            self.ensure_valid_next_state(active_sync_state[CURRENT_STATE_KEY])
            self.ensure_valid_next_action(
                active_sync_state[CURRENT_ACTION_KEY])

            path = get_path(active_sync_state, SYNC_STATE_FILE_KEY)
            with open(path, 'w', encoding='UTF-8') as file:
                json.dump(active_sync_state, file)
                file.close()

            current_state = self.states[active_sync_state[CURRENT_STATE_KEY]]

    def ensure_valid_next_state(self, next_state):
        if next_state not in self.states:
            raise StateMachineError(
                f'The proposed next state is unknown: "{next_state}". '
                f'Aborting. The unknown state has to be added to the '
                f'allowed list at configuration time.')

    def ensure_valid_next_action(self, next_action):
        if next_action not in self.actions:
            raise StateMachineError(
                f'The proposed next action is unknown: "{next_action}". '
                f'Aborting. The unknown action has to be added to the '
                f'allowed list at configuration time.')

    def get_state(self, name: str) -> State:
        return None if name not in self.states else self.states[name]
