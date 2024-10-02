# games/game_state.py
from abc import ABC, abstractmethod
from typing import List, Any

class GameState(ABC):

    @abstractmethod
    def get_current_player(self) -> int:
        pass

    @abstractmethod
    def get_valid_actions(self) -> List[Any]:
        pass

    @abstractmethod
    def is_terminal(self) -> bool:
        pass

    @abstractmethod
    def apply_action(self, action: Any) -> 'GameState':
        pass

    @abstractmethod
    def get_reward(self) -> float:
        """Returns the reward for the current state, assuming it's terminal."""
        pass

    @abstractmethod
    def render(self,show_valid_moves: bool=False) -> str:
        pass
