import tkinter as tk
from abc import ABC, abstractmethod
from functools import reduce
from tkinter import messagebox

from typing import List

from pydantic import BaseModel

# Player constants
PLAYER1_COLOR = 'red'  # Color for Player 1
PLAYER2_COLOR = 'blue'  # Color for Player 4


class Shape(ABC):
    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas

    @abstractmethod
    def draw(self):
        pass


class Point(Shape):
    def __init__(self, x: int, y: int, canvas: tk.Canvas) -> None:
        super().__init__(canvas)
        self.x = x
        self.y = y

    def draw(self):
        self.canvas.create_oval(self.x - 4, self.y - 4, self.x + 4, self.y + 4, fill='black')

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x


class Line(Shape):
    def __init__(self, p1: Point, p2: Point, color: str, canvas: tk.Canvas):
        super().__init__(canvas)
        self.p1 = p1 if p1 < p2 else p2
        self.p2 = p1 if p1 > p2 else p2
        self.color = color

    def draw(self):
        self.canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=self.color)

    def get_side(self):
        return self.color == PLAYER1_COLOR


class Box(Shape):
    def __init__(self, p1: Point, p2: Point, last_line: Line, canvas: tk.Canvas):
        super().__init__(canvas)
        self.p1 = p1
        self.p2 = p2
        self.last_line = last_line

    def get_side(self):
        return self.last_line.color == PLAYER1_COLOR

    def draw(self):
        self.canvas.create_rectangle(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=self.last_line.color)

