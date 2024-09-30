# %%
import numpy as np
from games.game_state import GameState
from games.othello_action import OthelloAction
from typing import List


class OthelloState(GameState):
    def __init__(self, board: np.ndarray, current_player: int):
        self.board = board
        self.current_player = current_player
        self.passes = 0

    def get_current_player(self) -> int:
        return self.current_player

    def get_valid_actions(self) -> List[OthelloAction]:
        valid_actions = []
        # Implement logic to find valid moves
        # For each cell, check if placing a disc results in flipping opponent's discs

        if not valid_actions:
            # No valid moves available; must pass
            valid_actions.append(OthelloAction.pass_action())
        return valid_actions

    def is_terminal(self) -> bool:
        # The game ends when both players pass consecutively
        return self.passes >= 2


    def apply_action(self, action: OthelloAction) -> 'OthelloState':
        new_board = self.board.copy()
        if action.is_pass:
            # No changes to the board; simply switch players
            new_state = OthelloState(new_board, -self.current_player, passes=self.passes + 1)
        else:
            # Reset pass count
            new_state = OthelloState(new_board, -self.current_player, passes=0)
            # Place the disc and flip opponent's discs accordingly
            # Implement flipping logic
        return new_state


    def get_reward(self) -> float:
        if not self.is_terminal():
            raise ValueError("Reward can only be calculated for terminal states.")
        black_discs = np.sum(self.board == 1)
        white_discs = np.sum(self.board == -1)
        if black_discs > white_discs:
            return 1.0  # Black wins
        elif black_discs < white_discs:
            return -1.0  # White wins
        else:
            return 0.0  # Draw


    def render(self) -> str:
        # Implement logic to render the board as a string
        pass

# %%
