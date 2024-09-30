from abc import ABC, abstractmethod

class Game(ABC):

    @abstractmethod
    def get_initial_state(self):
        """Returns the initial game state."""
        pass

    @abstractmethod
    def get_valid_actions(self, state):
        """Returns a list of valid actions from the given state."""
        pass

    @abstractmethod
    def is_terminal(self, state):
        """Checks if the given state is terminal."""
        pass

    @abstractmethod
    def get_next_state(self, state, action):
        """Returns the next state after applying the action to the current state."""
        pass

    @abstractmethod
    def get_reward(self, state):
        """Returns the reward for the given terminal state."""
        pass

    @abstractmethod
    def get_current_player(self, state):
        """Returns the player who has the turn in the given state."""
        pass

    @abstractmethod
    def render(self, state):
        """Prints or returns a string representation of the state (for debugging)."""
        pass
