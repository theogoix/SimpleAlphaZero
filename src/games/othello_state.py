# %%
import numpy as np
from games.state import GameState
from typing import List

class OthelloState(GameState):
    def __init__(self, board: np.ndarray, current_player: int):
        self.board = board
        self.current_player = current_player

    def get_current_player(self) -> int:
        return self.current_player

    def get_valid_actions(self) -> List['OthelloAction']:
        # Implement logic to find valid actions
        pass

    def is_terminal(self) -> bool:
        # Implement logic to check if the game has ended
        pass

    def apply_action(self, action: 'OthelloAction') -> 'OthelloState':
        # Implement logic to return a new state after applying the action
        pass

    def get_reward(self) -> float:
        # Implement logic to calculate reward if the state is terminal
        pass

    def render(self) -> str:
        # Implement logic to render the board as a string
        pass

# %%
