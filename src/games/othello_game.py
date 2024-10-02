# %%
import os
os.chdir("..")

# %%

import numpy as np
from games.game import Game
from games.othello_action import OthelloAction
from games.othello_state import OthelloState

class OthelloGame(Game):

    def get_initial_state(self) -> OthelloState:
        board = np.zeros((8, 8), dtype=int)
        # Set up initial four discs in the center
        board[3, 3] = board[4, 4] = -1  # White discs
        board[3, 4] = board[4, 3] = 1   # Black discs
        current_player = 1  # Black starts
        return OthelloState(board, current_player)
    
    
    def parse_move(self, move_str: str) -> OthelloAction:
        if move_str.lower() == 'pass':
            return OthelloAction.pass_action()
        if len(move_str) != 2 or move_str[0] not in 'abcdefgh' or not move_str[1].isdigit():
            raise ValueError("Invalid move format. Use format like 'd3' or 'pass'.")
        col = ord(move_str[0]) - ord('a')
        row = int(move_str[1]) - 1
        return OthelloAction(row, col)

    def play_interactive_game(self):
        state = self.get_initial_state()
        stop = False
        while not (stop or state.is_terminal()):
            state.render(show_valid_moves=True)
            current_player = 'Black' if state.get_current_player() == 1 else 'White'
            print(f"{current_player}'s turn.")
            valid_actions = state.get_valid_actions()
            if len(valid_actions) == 1 and valid_actions[0].is_pass:
                print("No valid moves available. Passing turn.")
                state = state.apply_action(valid_actions[0])
                continue
            move_made = False
            while not move_made:
                try:
                    move_input = input("Enter your move (e.g., 'd3') or 'pass': ")
                    if move_input.lower() == 'stop':
                        stop = True
                        break
                    action = self.parse_move(move_input)
                    if action not in valid_actions:
                        print("Invalid move. Try again.")
                    else:
                        state = state.apply_action(action)
                        move_made = True
                except ValueError as e:
                    print(str(e))
        # Game over
        state.render()
        reward = state.get_reward()
        if reward > 0:
            print("Black wins!")
        elif reward < 0:
            print("White wins!")
        else:
            print("It's a draw!")

# %%
game = OthelloGame()
game.play_interactive_game()
# %%
