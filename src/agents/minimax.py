from typing import Tuple

from agents.agent import Agent
from games.action import Action
from games.game_state import GameState


class MinimaxAgent(Agent):
    def __init__(self,depth=2):
        self.depth = depth

    def select_action(self, state: GameState, action_list: list[Action]) -> Action:
        _, action = self.negamax(state, self.depth, -2, 2, 1, MinimaxAgent.greedy)
        return action
    
    @staticmethod
    def negamax(state: GameState, depth: int, alpha: float, beta: float, color, eval_func) -> Tuple[int, Action]:
        if state.is_terminal():
            return state.get_current_player()  * state.get_reward(), None
        elif depth == 0:
            return state.get_current_player()  * eval_func(state), None
        
        max_score = -2
        best_action = None
        action_list = state.get_valid_actions()

        for action in action_list:
            new_state = state.apply_action(action=action)
            score, _ = MinimaxAgent.negamax(new_state, depth -1, -beta, -alpha, - color, eval_func)
            score = -score
            if score > max_score:
                max_score = score
                best_action = action
            
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        
        return max_score, best_action

    @staticmethod
    def greedy(state):
        return state.board.mean()


