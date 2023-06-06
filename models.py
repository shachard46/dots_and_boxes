import tkinter as tk
from abc import ABC, abstractmethod
from functools import reduce
from tkinter import messagebox

from typing import List, Union

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


class GameState:
    def __init__(self, points, lines, boxes):
        self.points: List[List[Point]] = points
        self.lines: List[List[Line]] = lines
        self.boxes: List[List[boxes]] = boxes


class Board:
    def __init__(self, board_size, points_distance, offset):
        self.root: tk.Tk = None
        self.canvas = None
        self.board_size = board_size
        self.points_distance = points_distance
        self.offset = offset
        self.lines: List[List[List[Union[Line, None]]]] = [[[None, None] for _ in range(board_size)] for _ in
                                                           range(board_size)]
        # self.h_lines: List[List[Line]] = [[None] * (board_size - 1) for _ in range(board_size)]
        # self.v_lines: List[List[Line]] = [[None] * board_size for _ in range(board_size - 1)]
        self.boxes: List[List[Box]] = [[None] * (board_size - 1) for _ in range(board_size - 1)]
        self.init_canvas()
        self.points: List[Point] = []
        self.draw_points()
        self.current_player = 0
        self.last_line: Line = None

    def switch_players(self):
        self.current_player = abs(self.current_player - 1)

    def init_canvas(self):
        self.root = tk.Tk()
        self.root.title("Dots and Boxes")
        canvas_size = self.board_size * self.points_distance * 2
        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size)
        self.canvas.pack()

    def start_game(self):
        self.root.mainloop()

    def draw_points(self):
        self.points = [
            [Point(self.offset + x * self.points_distance, self.offset + y * self.points_distance, self.canvas) for x in
             range(self.board_size)]
            for y in range(self.board_size)]
        for row in self.points:
            for point in row:
                point.draw()

    def get_color(self):
        return PLAYER1_COLOR if self.current_player else PLAYER2_COLOR

    def set_line(self, x1, y1, x2, y2):
        line = Line(self.points[y1][x1], self.points[y2][x2], self.get_color(), self.canvas)
        if x1 == x2 and abs(y1 - y2) == 1 and y1 < self.board_size and y2 < self.board_size:
            pos = 1
        elif y1 == y2 and abs(x2 - x1) == 1 and x1 < self.board_size and x2 < self.board_size:
            pos = 0
        else:
            print('points are illegal')
            return
        if self.lines[min(y1, y2)][min(x1, x2)][pos]:
            return
        self.lines[min(y1, y2)][min(x1, x2)][pos] = line
        line.draw()
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

    def check_game_over(self):
        if all(all(row) for row in self.boxes):
            count_player1 = 0
            count_player2 = 0
            for box in reduce(lambda a, b: a + b, self.boxes):
                count_player1 += 1 if box.get_side() else 0
                count_player2 += 0 if box.get_side() else 1

            if count_player1 > count_player2:
                winner = "Player 1 wins!"
            elif count_player2 > count_player1:
                winner = "Player 2 wins!"
            else:
                winner = "It's a tie!"

            # Show the winner in a message box
            messagebox.showinfo("Game Over", winner)
            self.root.quit()  # Close the window

    def get_game_state(self) -> GameState:
        return GameState(lines=self.lines, points=self.points,
                         boxes=self.boxes)

-
|