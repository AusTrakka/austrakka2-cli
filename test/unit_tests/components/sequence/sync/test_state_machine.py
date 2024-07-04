import pytest

from austrakka.components.sequence.sync.sync_workflow import configure_state_machine
from austrakka.components.sequence.sync.state_machine import *


class TestStateMachine:

    def test_run_given_next_action_is_unknown_expect_error(self):
        with pytest.raises(StateMachineError) as ex:
            sm = configure_state_machine()
            sync_state = {
                CURRENT_STATE_KEY: SName.UP_TO_DATE,
                CURRENT_ACTION_KEY: "SOME-UNKNOWN-VALUE"
            }
            sm.run(sync_state)

        assert f'The proposed next action is unknown:' \
               f' "SOME-UNKNOWN-VALUE". ' in str(ex.value)

    def test_run_given_next_state_is_unknown_expect_error(self):
        with pytest.raises(StateMachineError) as ex:
            sm = configure_state_machine()
            sync_state = {
                CURRENT_STATE_KEY: "SOME-UNKNOWN-VALUE",
                CURRENT_ACTION_KEY: Action.pull_manifest
            }
            sm.run(sync_state)

        assert f'The proposed next state is unknown:' \
               f' "SOME-UNKNOWN-VALUE". ' in str(ex.value)
