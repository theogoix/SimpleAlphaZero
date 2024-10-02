from games.game_state import GameState
from games.action import Action
from agents.agent import Agent
from numpy import np

class RandomAgent(Agent):
    def __init__(self,rng_seed=42):
        self.rng = np.random(seed=rng_seed)
    
    def select_action(self, state: GameState, action_list: list[Action]) -> Action:
        return self.rng.choice(action_list)