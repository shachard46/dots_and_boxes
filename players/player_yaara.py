import random
from typing import Tuple

from game_blocks.game_state import GameState
from game_blocks.player import Player


class RandomPlayer(Player):
    def __init__(self, name: str, color: str):
        super().__init__(name, color)

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        x1 = random.randint(0, len(game_state.lines) - 1)
        x2 = x1 + random.randint(0, 1)
        y1 = random.randint(0, len(game_state.lines) - 1)
        y2 = y1 + 1 if x1 == x2 else y1
        return x1, y1, x2, y2


class SmartRandomPlayer(Player):
    def __init__(self, name: str, color: str):
        super().__init__(name, color)

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        empty_lines = []
        for row_ind, row in enumerate(game_state.lines):
            for col_ind, col in enumerate(row):
                for line_ind, line in enumerate(col):
                    if line is None:
                        row_increment = 1 if line_ind == 1 else 0
                        col_increment = 1 if line_ind == 0 else 0
                        if row_ind + row_increment < len(game_state.lines) and col_ind + col_increment < len(
                                game_state.lines):
                            empty_lines.append((col_ind, row_ind, col_ind + col_increment, row_ind + row_increment))

        return random.choice(empty_lines)


class VerySmartRandomPlayer(Player):
    def __init__(self, name: str, color: str):
        super().__init__(name, color)

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        for row_ind, row in enumerate(game_state.lines[:-1]):
            for col_ind, col in enumerate(row[:-1]):
                if col[0] and col[1] and row[col_ind + 1][1] and not game_state.lines[row_ind + 1][col_ind][0]:
                    return col_ind, row_ind + 1, col_ind + 1, row_ind + 1
                if not col[0] and col[1] and row[col_ind + 1][1] and game_state.lines[row_ind + 1][col_ind][0]:
                    return col_ind, row_ind, col_ind + 1, row_ind
                if col[0] and not col[1] and row[col_ind + 1][1] and game_state.lines[row_ind + 1][col_ind][0]:
                    return col_ind, row_ind, col_ind, row_ind + 1
                if col[0] and col[1] and not row[col_ind + 1][1] and game_state.lines[row_ind + 1][col_ind][0]:
                    return col_ind + 1, row_ind, col_ind + 1, row_ind + 1

        empty_lines = []
        for row_ind, row in enumerate(game_state.lines):
            for col_ind, col in enumerate(row):
                for line_ind, line in enumerate(col):
                    if line is None:
                        row_increment = 1 if line_ind == 1 else 0
                        col_increment = 1 if line_ind == 0 else 0
                        if row_ind + row_increment < len(game_state.lines) and col_ind + col_increment < len(
                                game_state.lines):
                            empty_lines.append((col_ind, row_ind, col_ind + col_increment, row_ind + row_increment))

        return random.choice(empty_lines)
