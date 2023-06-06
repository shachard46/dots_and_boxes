import random
from typing import Tuple

from models.board import GameState
from models.player import Player


class SmartPlayer(Player):
    def __init__(self, name: str, color: str):
        super().__init__(name, color)

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        x1 = random.randint(0, 4)
        x2 = x1 + random.randint(0, 1)
        y1 = random.randint(0, 4)
        y2 = y1 + 1 if x1 == x2 else y1
        return x1, y1, x2, y2
