# %%
import numpy as np
from games.game_state import GameState
from games.othello_action import OthelloAction
from typing import List



def shift_board(board: np.ndarray, dx: int, dy: int) -> np.ndarray:
    """
    Shift the board in the specified direction (dx, dy) without wrapping.
    Vacated cells are filled with 0 to prevent incorrect detections.

    :param board: The current game board as a NumPy array.
    :param dx: Direction to shift in rows (-1, 0, 1).
    :param dy: Direction to shift in columns (-1, 0, 1).
    :return: The shifted board as a NumPy array.
    """
    shifted = np.roll(board, shift=(dx, dy), axis=(0, 1))
    
    # Handle wrapping by setting the rolled-over edges to 0
    if dx > 0:
        shifted[:dx, :] = 0
    elif dx < 0:
        shifted[dx:, :] = 0
    if dy > 0:
        shifted[:, :dy] = 0
    elif dy < 0:
        shifted[:, dy:] = 0
    return shifted


class OthelloState(GameState):
    DIRECTIONS = [(-1, -1), (-1, 0), (-1,1),
                  (0 , -1),          (0, 1),
                  (1 , -1), (1, 0) , (1, 1)]
    
    def __init__(self, board: np.ndarray, current_player: int, passes: int = 0):
        self.board = board.copy()
        self.current_player = current_player
        self.passes = passes

    def get_initial_state() -> 'OthelloState':
        board = np.zeros((8,8), dtype=int)
        board[3,3] = board[4,4] = -1
        board[3,4] = board [4,3] = 1
        current_player = 1
        return OthelloState(board=board, current_player=current_player)

    def get_current_player(self) -> int:
        return self.current_player


    def get_valid_actions(self) -> List[OthelloAction]:
        """
        Get a list of all valid actions for the current player using an optimized NumPy approach.

        :return: A list of OthelloAction instances representing valid moves.
        """
        player = self.current_player
        opponent = -player
        valid_moves = np.zeros_like(self.board, dtype=bool)
        empty = (self.board == 0)

        # Iterate over all directions
        for dx, dy in self.DIRECTIONS:
            # Shift the board in the direction (dx, dy)
            shifted = shift_board(self.board, dx, dy)
            candidates = empty & (shifted == opponent)
            valid_dir = np.zeros_like(self.board, dtype=bool)
            for _ in range(6):
                shifted = shift_board(shifted, dx=dx, dy=dy)
                valid_dir |= (candidates & (shifted == player))
                candidates &= (shifted == opponent)
            valid_moves |= valid_dir

        # Extract the row and column indices of valid moves
        move_indices = np.argwhere(valid_moves)
        valid_actions = [OthelloAction(row=int(r), col=int(c)) for r, c in move_indices]
        
        # If no valid moves are found, consider adding a pass action
        if not valid_actions:
            valid_actions.append(OthelloAction(row=-1, col=-1, is_pass=True))  # Using (-1, -1) to denote pass
        
        return valid_actions


    def _shift(self, board:np.ndarray, dr: int, dc: int) -> np.ndarray:
        shifted = np.roll(board, shift=(dr, dc), axis=(0,1))

        if dr > 0:
            shifted[:dr, :] = 0
        elif dr < 0:
            shifted[dr:, :] = 0
        if dc > 0:
            shifted[:, :dc] = 0
        elif dc < 0:
            shifted[:, dc:] = 0
        return shifted

    def is_terminal(self) -> bool:
        # The game ends when both players pass consecutively
        return self.passes >= 2


    
    def apply_action(self, action: OthelloAction) -> 'OthelloState':
        """
        Apply an action to the current state and return the new state.

        :param action: An OthelloAction instance representing the move to apply.
        :return: A new OthelloState instance after applying the move.
        :raises ValueError: If the action is invalid.
        """
        if action.is_pass:
            # Handle pass action
            next_player = -self.current_player
            return OthelloState(self.board, next_player, passes=self.passes + 1)
        
        if not (0 <= action.row < 8 and 0 <= action.col < 8):
            raise ValueError(f"Action ({action.row}, {action.col}) is out of bounds.")
        if self.board[action.row, action.col] != 0:
            raise ValueError(f"Cell ({action.row}, {action.col}) is not empty.")

        # First, verify that the action is valid
        valid_actions = self.get_valid_actions()
        if action not in valid_actions:
            raise ValueError(f"Action ({action.row}, {action.col}) is not a valid move.")

        # Create a copy of the board to apply changes
        new_board = self.board.copy()
        new_board[action.row, action.col] = self.current_player

        opponent = -self.current_player

        # Initialize a mask for all cells to flip
        flip_mask = np.zeros((8, 8), dtype=bool)

        for dr, dc in self.DIRECTIONS:
            # Initialize masks for this direction
            cells = []
            r, c = action.row + dr, action.col + dc

            # Traverse in the current direction
            while 0 <= r < 8 and 0 <= c < 8:
                current_cell = new_board[r, c]
                if current_cell == opponent:
                    cells.append((r, c))
                elif current_cell == self.current_player:
                    if cells:
                        # Mark these cells to be flipped
                        rows, cols = zip(*cells)
                        flip_mask[rows, cols] = True
                    break
                else:
                    break
                r += dr
                c += dc

        # Apply flipping using the mask
        new_board[flip_mask] = self.current_player

        # Switch the current player
        next_player = opponent

        # Return the new state
        return OthelloState(new_board, next_player, passes=0)

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


    def render(self, show_valid_moves=False):
        board_str = '  a  b  c  d  e  f  g  h\n'
        valid_moves = []
        if show_valid_moves:
            valid_moves = [(action.row, action.col) for action in self.get_valid_actions() if not action.is_pass]

        for row in range(8):
            board_str += str(row + 1)  # Row numbers
            for col in range(8):
                cell = self.board[row, col]
                if (row, col) in valid_moves:
                    board_str += ' * '  # Indicate valid move
                elif cell == 1:
                    board_str += ' B '
                elif cell == -1:
                    board_str += ' W '
                else:
                    board_str += ' . '
            board_str += '\n'
        print(board_str)

# %%

def initialize_test_board() -> np.ndarray:
    board = np.zeros((8, 8), dtype=int)
    # Manually setting up the board as per the test scenario
    # Rows and columns are 0-indexed
    # Setting black discs (B = -1)
    board[2, 3] = -1  # c4
    board[3, 3] = -1  # d4
    board[3, 4] = -1  # e4
    board[4, 3] = -1  # d5
    board[4, 5] = -1  # f5
    board[5, 5] = -1  # f6
    board[6, 5] = -1  # f7

    # Setting white discs (W = 1)
    board[3, 5] = 1    # f4
    board[4, 4] = 1    # e5
    board[4, 5] = 1    # f5 (This seems conflicting; adjust accordingly)
    
    # Note: The user mentioned 'f8', which is (7, 5), but in the initial description,
    # row 8 has only a '*' at (7,6) (0-based index)
    
    # Adjusting based on the description:
    # Let's ensure that f8 (row 7, column 5) is empty and has three black discs above to be flipped
    # So, positions f5 (4,5), f6 (5,5), f7 (6,5) should be black, and f8 (7,5) empty initially
    # But in the previous assignments, f5 was set to -1 and 1, which is conflicting
    # Correcting:
    board[4, 5] = -1  # f5
    board[5, 5] = -1  # f6
    board[6, 5] = -1  # f7
    board[7, 5] = 0   # f8 remains empty

    # Setting white discs correctly
    board[3, 5] = 1    # f4
    board[4, 4] = 1    # e5
    
    return board

def print_valid_actions(valid_actions: List[OthelloAction]):
    print("Valid actions:")
    for action in sorted(valid_actions, key=lambda x: (x.row, x.col)):
        if action.is_pass:
            print("Pass")
        else:
            # Convert 0-based indices to chess-like notation (a-h, 1-8)
            col_letter = chr(ord('a') + action.col)
            row_number = action.row + 1
            print(f"{col_letter}{row_number}")

# Initialize the test board
test_board = initialize_test_board()
state = OthelloState(test_board, current_player=1)  # Assuming it's black's turn

# Display the initial state
print("Initial Test Board State:")
state.render()

# Get valid actions for the current player (black)
valid_actions = state.get_valid_actions()
print("\nValid actions for player B:")
print_valid_actions(valid_actions)


# %%
