from typing import Tuple

from models.board import GameState


class Player:
    def __init__(self, name: str):
        self.name = name

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        raise NotImplementedError
