# mcts_node.py
import math

from games.game_state import GameState


class MCTSNode:
    def __init__(self, state: GameState, parent=None, prior=0.0):
        self.state = state
        self.parent = parent
        self.children = {}  # action -> MCTSNode
        self.visit_count = 0
        self.total_value = 0.0
        self.prior = prior  # P(s, a)
        self.is_expanded = False

    @property
    def mean_value(self):
        return self.total_value / self.visit_count if self.visit_count > 0 else 0.0

# mcts.py

class MCTS:
    def __init__(self, neural_network, config):
        self.neural_network = neural_network
        self.config = config  # Hyperparameters like c_puct, number of simulations

    def search(self, initial_state: GameState):
        root = MCTSNode(state=initial_state)
        policy, value = self.neural_network.predict(initial_state)
        self.expand_node(root, policy)

        for _ in range(self.config['num_simulations']):
            node = root
            search_path = [node]

            # Selection
            while node.is_expanded and not node.state.is_terminal():
                action, node = self.select_child(node)
                search_path.append(node)

            # Evaluation
            if not node.state.is_terminal():
                policy, value = self.neural_network.predict(node.state)
                self.expand_node(node, policy)
            else:
                value = node.state.get_reward()

            # Backpropagation
            self.backpropagate(search_path, value)

        return self.get_action_probs(root)




    def select_child(self, node):
        best_score = -float('inf')
        best_action = None
        best_child = None

        for action, child in node.children.items():
            ucb_score = self.ucb_score(node, child)
            if ucb_score > best_score:
                best_score = ucb_score
                best_action = action
                best_child = child

        return best_action, best_child

    def ucb_score(self, parent, child):
        c_puct = self.config['c_puct']
        pb_c = c_puct * child.prior * math.sqrt(parent.visit_count) / (1 + child.visit_count)
        return child.mean_value + pb_c


    def expand_node(self, node, policy):
        node.is_expanded = True
        valid_actions = node.state.get_valid_actions()
        policy_probs = policy.detach().numpy()
    
        for action in valid_actions:
            action_index = action.to_index()
            child_state = node.state.apply_action(action)
            prior = policy_probs[action_index]
            child_node = MCTSNode(state=child_state, parent=node, prior=prior)
            node.children[action] = child_node


    def backpropagate(self, search_path, value):
        for node in reversed(search_path):
            node.visit_count += 1
            node.total_value += value if node.state.get_current_player() == search_path[0].state.get_current_player() else -value


    def get_action_probs(self, root):
        action_visits = [(action, child.visit_count) for action, child in root.children.items()]
        total_visits = sum(visits for action, visits in action_visits)
        action_probs = {action: visits / total_visits for action, visits in action_visits}
        return action_probs

    # Implement other methods...
