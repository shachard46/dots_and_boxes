import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox

from typing import List

# Game constants
DOT_SIZE = 40  # Size of each dot on the grid
GRID_SIZE = 6  # Number of dots in each row and column
CANVAS_SIZE = (GRID_SIZE - 1) * DOT_SIZE  # Size of the canvas

# Player constants
PLAYER1_COLOR = 'red'  # Color for Player 1
PLAYER4_COLOR = 'blue'  # Color for Player 4

# Game state variables
current_player = 1
lines_drawn = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
boxes_owned = [[0] * (GRID_SIZE - 1) for _ in range(GRID_SIZE - 1)]


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


class Line(Shape):
    def __init__(self, p1: Point, p2: Point, color: str, canvas: tk.Canvas):
        super().__init__(canvas)
        self.p1 = p1
        self.p2 = p2
        self.color = color

    def draw(self):
        self.canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=self.color)

    def get_side(self):
        return self.color == 'red'


class Box(Shape):
    def __init__(self, p1: Point, p2: Point, last_line: Line, canvas: tk.Canvas):
        super().__init__(canvas)
        self.p1 = p1
        self.p2 = p2
        self.last_line = last_line

    def draw(self):
        self.canvas.create_rectangle(self.p1.x, self.p1.y, self.p1.x, self.p2.y, fill=self.last_line.color)


class Board:
    def __init__(self, board_size, points_distance):
        self.canvas = None
        self.board_size = board_size
        self.points_distance = points_distance
        self.h_lines: List[List[Line]] = [[None] * (board_size - 1)] * board_size
        self.v_lines: List[List[Line]] = [[None] * board_size] * (board_size - 1)
        self.boxes: List[List[Box]] = [[None] * (board_size - 1)] * (board_size - 1)
        self.points: List[Point] = []
        self.draw_points()
        self.current_player = 0
        self.last_line: Line = None

    def switch_players(self):
        self.current_player = abs(self.current_player - 1)

    def init_canvas(self):
        root = tk.Tk()
        root.title("Dots and Boxes")
        canvas_size = self.board_size * self.points_distance * 2
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size)
        self.canvas.pack()

    def draw_points(self):
        self.points = [
            [Point(x * self.points_distance, y * self.points_distance, self.canvas) for x in range(self.board_size)]
            for y in range(self.board_size)]
        for row in self.points:
            for point in row:
                point.draw()

    def get_color(self):
        return 'red' if self.current_player else 'blue'

    def set_line(self, x1, y1, x2, y2):
        line = Line(self.points[x1][y1], self.points[x2][y2], self.get_color(), self.canvas)
        if x1 == x2:
            if not self.h_lines[x1][y1]:
                self.h_lines[x1][y1] = line
        if y1 == y2:
            if not self.v_lines[x1][y1]:
                self.v_lines[x1][y1] = line
        else:
            return
        self.last_line = line
        self.check_completed_boxes()
        self.switch_players()

    def check_completed_boxes(self):
        for i in range(self.board_size - 1):
            for j in range(self.board_size - 1):
                if self.h_lines[i][j] and self.h_lines[i + 1][j] and self.v_lines[i][j] and self.v_lines[i][j + 1]:
                    self.boxes[i][j] = Box(self.h_lines[i][j].p1, self.h_lines[i + 1][j].p2, self.last_line,
                                           self.canvas)
                    self.boxes[i][j].draw()
