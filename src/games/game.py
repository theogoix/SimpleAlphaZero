# games/game.py
from abc import ABC, abstractmethod
from typing import List
from games.state import State
from games.action import Action

class Game(ABC):

    @abstractmethod
    def get_initial_state(self) -> State:
        pass

    @abstractmethod
    def get_valid_actions(self, state: State) -> List[Action]:
        pass

    @abstractmethod
    def is_terminal(self, state: State) -> bool:
        pass

    @abstractmethod
    def get_next_state(self, state: State, action: Action) -> State:
        pass

    @abstractmethod
    def get_reward(self, state: State) -> float:
        pass

    @abstractmethod
    def get_current_player(self, state: State) -> int:
        pass

    @abstractmethod
    def render(self, state: State) -> str:
        pass

