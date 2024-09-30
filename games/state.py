from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def get_current_player(self):
        """Returns the player who has the turn in this state."""
        pass

    @abstractmethod
    def is_terminal(self):
        """Checks if the state is terminal."""
        pass

    @abstractmethod
    def get_valid_actions(self):
        """Returns a list of valid actions from this state."""
        pass

    @abstractmethod
    def render(self):
        """Returns a string representation of the state."""
        pass
