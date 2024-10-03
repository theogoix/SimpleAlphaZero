# %%
import os
os.chdir("..")

# %%

import numpy as np
from games.game import Game
from games.othello_action import OthelloAction
from games.othello_state import OthelloState
from agents.agent import Agent

class OthelloGame(Game):

    def __init__(self,rng_seed=42):
        self.state = self.get_initial_state()
        self.rng = np.random.default_rng(seed=rng_seed)
        self.history: list[OthelloState,OthelloAction] = []

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


    def play_random_game(self):
        rng = np.random.default_rng(seed=42)
        state = self.get_initial_state()
        while not state.is_terminal():
            #state.render(show_valid_moves=True)

            possible_moves = state.get_valid_actions()
            chosen_action = rng.choice(possible_moves)
            self.history.append((state,chosen_action))
            state = state.apply_action(chosen_action)
        state.render(show_valid_moves=True)
        print(state.get_reward())
        return self.history

    def play_game_with_agents(self,black_agent:Agent,white_agent:Agent,render=True) -> list[OthelloState,OthelloAction]:
        state = self.get_initial_state()
        move_count = 0
        history = []
        while not state.is_terminal():
            agent = black_agent if move_count % 2 == 0 else white_agent
            action_list = state.get_valid_actions()
            chosen_action = agent.select_action(state=state, action_list=action_list)
            history.append((state,chosen_action))
            state = state.apply_action(chosen_action)
        if render:
            state.render()
            print(state.get_reward())
        return state.get_reward()

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
from agents.random_agent import RandomAgent, HumanAgent
from agents.minimax import MinimaxAgent
from tqdm import tqdm

game = OthelloGame()
human_agent = HumanAgent()
random_agent = RandomAgent(seed=35)
minimax_agent = MinimaxAgent(depth=3)
first_win = 0
second_win = 0
draws = 0
for i in tqdm(range(9)):
    if i%2 == 0:
        result = game.play_game_with_agents(minimax_agent,random_agent,render=False)
    else:
        result = - game.play_game_with_agents(random_agent,minimax_agent,render=False)
    if result == 0:
        draws += 1
    elif result == 1:
        first_win += 1
    else:
        second_win += 1
    
print(f"{first_win=}, {draws=}, {second_win=}")
# %%
