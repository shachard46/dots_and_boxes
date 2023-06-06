from typing import List, Union

from game_blocks.shapes import Point, Line, Box


class GameState:
    def __init__(self, points, lines, boxes):
        self.points: List[List[Point]] = points
        self.lines: List[List[List[Union[Line, None]]]] = lines
        self.boxes: List[List[Box]] = boxes

    def copy(self):
        return GameState(self.points.copy(), self.lines.copy(), self.boxes.copy())
