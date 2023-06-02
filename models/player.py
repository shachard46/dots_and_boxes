from pydantic import BaseModel
from typing import List, Callable, Tuple

from models import Line, Box, Point, GameState, Board


class Player:
    def __init__(self, action: Callable[[GameState], Tuple[int, int, int, int]]):
        self.action = action
