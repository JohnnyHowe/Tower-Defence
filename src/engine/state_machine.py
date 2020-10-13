

class StateMachine:
    """ Basic state machine """

    _current_state = 0

    def set_state(self, new_state):
        self._current_state = new_state

    def get_state(self):
        return self._current_state

    def is_in_state(self, state):
        return state == self._current_state
