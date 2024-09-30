# games/othello_action.py

from dataclasses import dataclass

@dataclass(frozen=True)
class OthelloAction:
    row: int = None
    col: int = None
    is_pass: bool = False

    @staticmethod
    def pass_action():
        return OthelloAction(is_pass=True)

    def to_index(self) -> int:
        if self.is_pass:
            return 64  # Index for pass action
        else:
            return self.row * 8 + self.col  # Index for board positions

    @staticmethod
    def from_index(index: int) -> 'OthelloAction':
        if index == 64:
            return OthelloAction.pass_action()
        else:
            row = index // 8
            col = index % 8
            return OthelloAction(row, col)
