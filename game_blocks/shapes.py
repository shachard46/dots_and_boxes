import tkinter as tk
from abc import ABC, abstractmethod

# Player constants
from typing import List

PLAYER1_COLOR = 'red'  # Color for Player 1
PLAYER2_COLOR = 'blue'  # Color for Player 4


class Shape(ABC):
    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas

    @abstractmethod
    def draw(self):
        pass


class Point(Shape):
    def __init__(self, x: int, y: int, canvas: tk.Canvas, point_size) -> None:
        super().__init__(canvas)
        self.x = x
        self.y = y
        self.point_size = point_size

    def draw(self):
        self.canvas.create_oval(self.x - self.point_size, self.y - self.point_size, self.x + self.point_size,
                                self.y + self.point_size, fill='black')

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x

    def copy(self) -> 'Point':
        return Point(self.x, self.y)


class Line(Shape):
    def __init__(self, p1: Point, p2: Point, color: str, canvas: tk.Canvas):
        super().__init__(canvas)
        self.p1 = p1 if p1 < p2 else p2
        self.p2 = p1 if p1 > p2 else p2
        self.color = color

    def draw(self):
        self.canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=self.color, width=3)

    def get_side(self, player_color):
        return self.color == player_color

    def copy(self) -> 'Line':
        return Line(self.p1.copy(), self.p2.copy(), self.color, self.canvas)


class Box(Shape):
    def __init__(self, p1: Point, p2: Point, last_line: Line, canvas: tk.Canvas):
        super().__init__(canvas)
        self.p1 = p1
        self.p2 = p2
        self.last_line = last_line

    def get_side(self, player_color):
        return self.last_line.color == player_color

    def draw(self):
        self.canvas.create_rectangle(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=self.last_line.color)

    def copy(self) -> 'Box':
        return Box(self.p1.copy(), self.p2.copy(), self.last_line.copy(), self.canvas)
