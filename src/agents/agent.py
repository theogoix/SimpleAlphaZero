from abc import ABC, abstractmethod
from games.action import Action
from games.game_state import GameState

class Agent(ABC):
    @abstractmethod
    def select_action(self, state: GameState, action_list: list[Action]) -> Action:
        pass