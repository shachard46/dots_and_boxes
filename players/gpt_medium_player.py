import random
from typing import Tuple, List, Union

from models.player import GameState
from models.shapes import Point, Line, Box


class WinningPlayer:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        # Check for any boxes that can be completed in the current turn
        for row in game_state.boxes:
            for box in row:
                if box:
                    if box.last_line is not None:
                        continue  # Box already completed

                lines = box.get_lines()
                opponent_lines = [line for line in lines if line.color != self.color]
                empty_lines = [line for line in lines if line.color is None]

                if len(opponent_lines) == 3 and len(empty_lines) == 1:
                    # Only one empty line left to complete the box
                    empty_line = empty_lines[0]
                    x1, y1 = empty_line.p1.x, empty_line.p1.y
                    x2, y2 = empty_line.p2.x, empty_line.p2.y
                    return x1, y1, x2, y2

        # If no boxes can be completed, choose a random valid line
        valid_lines = []
        for row in game_state.lines:
            for line_pair in row:
                if line_pair[0] and line_pair[0].color != self.color and line_pair[1] is None:
                    valid_lines.append((line_pair[0].p1, line_pair[0].p2))
                if line_pair[1] and line_pair[1].color != self.color and line_pair[0] is None:
                    valid_lines.append((line_pair[1].p1, line_pair[1].p2))

        if valid_lines:
            chosen_line = random.choice(valid_lines)
            x1, y1 = chosen_line[0].x, chosen_line[0].y
            x2, y2 = chosen_line[1].x, chosen_line[1].y
            return x1, y1, x2, y2
        else:
            # No valid lines available, return default values
            return 0, 0, 0, 0
