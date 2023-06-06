from typing import Tuple

from models.board import GameState


class Player:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        return 0, 0, 1, 0
