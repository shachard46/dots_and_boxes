from functools import reduce
from tkinter import messagebox
from typing import List, Union
import tkinter as tk

from models.player import Player
from models.shapes import Point, Line, Box, PLAYER1_COLOR, PLAYER2_COLOR


class GameState:
    def __init__(self, points, lines, boxes):
        self.points: List[List[Point]] = points
        self.lines: List[List[List[Union[Line, None]]]] = lines
        self.boxes: List[Box] = boxes


class Board:
    def __init__(self, board_size, points_distance, offset, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self._root: tk.Tk = None
        self._canvas = None
        self.board_size = board_size
        self._points_distance = points_distance
        self._offset = offset
        self.lines: List[List[List[Union[Line, None]]]] = [[[None, None] for column in range(board_size)] for row in
                                                           range(board_size)]
        self.boxes: List[List[Box]] = [[None] * (board_size - 1) for _ in range(board_size - 1)]
        self._init_canvas()
        self.points: List[Point] = []
        self._draw_points()
        self.current_player = player1
        self.last_line: Line = None

    def get_root(self):
        return self._root

    def _switch_players(self):
        self.current_player = self.player1 if self.player1 else self.player2

    def _init_canvas(self):
        self._root = tk.Tk()
        self._root.title("Dots and Boxes")
        canvas_size = self.board_size * self._points_distance * 2
        self._canvas = tk.Canvas(self._root, width=canvas_size, height=canvas_size)
        self._canvas.pack()

    def start_game(self):
        self._root.mainloop()

    def _draw_points(self):
        self.points = [
            [Point(self._offset + x * self._points_distance, self._offset + y * self._points_distance, self._canvas) for
             x in
             range(self.board_size)]
            for y in range(self.board_size)]
        for row in self.points:
            for point in row:
                point.draw()

    def get_color(self):
        return self.current_player.color

    def set_line(self, x1, y1, x2, y2):
        if y1 > self.board_size or y2 > self.board_size or x1 > self.board_size or x2 > self.board_size:
            return
        if x1 == x2 and abs(y1 - y2) == 1:
            pos = 1
        elif y1 == y2 and abs(x2 - x1) == 1:
            pos = 0
        else:
            print('points are illegal')
            return
        if self.lines[min(y1, y2)][min(x1, x2)][pos]:
            return
        line = Line(self.points[y1][x1], self.points[y2][x2], self.get_color(), self._canvas)
        self.lines[min(y1, y2)][min(x1, x2)][pos] = line
        line.draw()
        self.last_line = line
        self.check_completed_boxes()
        self._switch_players()

    def check_completed_boxes(self):
        for i in range(self.board_size - 1):
            for j in range(self.board_size - 1):
                if self.lines[i][j][0] and self.lines[i][j][1] and self.lines[i + 1][j][0] and self.lines[i][j + 1][1]:
                    if self.boxes[i][j]:
                        continue
                    self.boxes[i][j] = Box(self.lines[i][j][0].p1, self.lines[i + 1][j][0].p2, self.last_line,
                                           self._canvas)
                    self.boxes[i][j].draw()
                    self._switch_players()

    def check_game_over(self):
        if all(all(row) for row in self.boxes):
            count_player1 = 0
            count_player2 = 0
            for box in reduce(lambda a, b: a + b, self.boxes):
                count_player1 += 1 if box.get_side(self.player1.color) else 0
                count_player2 += 1 if box.get_side(self.player2.color) else 0

            if count_player1 > count_player2:
                winner = "Player 1 wins!"
            elif count_player2 > count_player1:
                winner = "Player 2 wins!"

            else:
                winner = "It's a tie!"

            # Show the winner in a message box
            messagebox.showinfo("Game Over", winner)
            self._root.quit()  # Close the window
            return False
        return True

    def get_game_state(self) -> GameState:
        return GameState(lines=self.lines, points=self.points,
                         boxes=self.boxes)
