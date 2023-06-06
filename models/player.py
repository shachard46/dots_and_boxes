from typing import Tuple, List, Union

from models.shapes import Point, Line, Box


class GameState:
    def __init__(self, points, lines, boxes):
        self.points: List[List[Point]] = points
        self.lines: List[List[List[Union[Line, None]]]] = lines
        self.boxes: List[Box] = boxes


class Player:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        return 0, 0, 1, 0
