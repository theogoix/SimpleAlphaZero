from games.game_state import GameState
from games.action import Action
from agents.agent import Agent
import numpy as np

class RandomAgent(Agent):
    def __init__(self,seed=42):
        self.rng = np.random.default_rng(seed=seed)
    
    def select_action(self, state: GameState, action_list: list[Action]) -> Action:
        return self.rng.choice(action_list)

class HumanAgent(Agent):
    def select_action(self, state: GameState, action_list: list[Action]) -> Action:
        move_made = False

        state.render(show_valid_moves=True)
        current_player = 'Black' if state.get_current_player() == 1 else 'White'
        print(f"{current_player}'s turn.")
        valid_actions = action_list
        if len(valid_actions) == 1 and valid_actions[0].is_pass:
            print("No valid moves available. Passing turn.")
            return valid_actions[0]
        human_readable_list = [action.to_string() for action in valid_actions]
        while not move_made:
            try:
                move_input = input("Enter your move (e.g., 'd3') or 'pass': ").lower()
                if move_input == 'stop':
                    stop = True
                    break
                
                if move_input in human_readable_list:
                    i = human_readable_list.index(move_input)
                    return valid_actions[i]
                else:
                    print("Invalid move. Try again.")
                    print(f"Available moves are:\n {' '.join(human_readable_list)}")
            except ValueError as e:
                print(str(e))