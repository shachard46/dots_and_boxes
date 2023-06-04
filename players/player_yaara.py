from typing import Tuple

from models.board import GameState
from models.player import Player


class SmartPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        pass
