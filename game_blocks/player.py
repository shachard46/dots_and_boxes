from typing import Tuple

from game_blocks.game_state import GameState


class Player:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        raise NotImplementedError
