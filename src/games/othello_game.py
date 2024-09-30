from games.game import Game

class OthelloGame(Game):
    
    
    
    def get_current_player(self, state):
        return super().get_current_player(state)
    def get_initial_state(self):
        return super().get_initial_state()
    def get_next_state(self, state, action):
        return super().get_next_state(state, action)
    def get_reward(self, state):
        return super().get_reward(state)
    def get_valid_actions(self, state):
        return super().get_valid_actions(state)
    def is_terminal(self, state):
        return super().is_terminal(state)
    def render(self, state):
        return super().render(state)
