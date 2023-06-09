from functools import reduce
from tkinter import messagebox
from typing import List
import tkinter as tk
from models.shapes import Point, Line, Box, PLAYER1_COLOR, PLAYER2_COLOR


class GameState:
    def __init__(self, points, horizontal_lines, vertical_lines, boxes):
        self.points: List[List[Point]] = points
        self.horizontal_lines: List[List[Line]] = horizontal_lines
        self.vertical_lines: List[List[Line]] = vertical_lines
        self.boxes: List[Box] = boxes


class Board:
    def __init__(self, board_size, points_distance, offset):
        self.root: tk.Tk = None
        self.canvas = None
        self.board_size = board_size
        self.points_distance = points_distance
        self.offset = offset
        self.h_lines: List[List[Line]] = [[None] * (board_size - 1) for _ in range(board_size)]
        self.v_lines: List[List[Line]] = [[None] * board_size for _ in range(board_size - 1)]
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
        if x1 == x2 and abs(y1 - y2) == 1:
            if self.v_lines[min(y1, y2)][x1]:
                return
            self.v_lines[min(y1, y2)][x1] = line
        elif y1 == y2 and abs(x2 - x1) == 1:
            if self.h_lines[y1][min(x1, x2)]:
                return
            self.h_lines[y1][min(x1, x2)] = line
        else:
            print('points are illegal')
            return
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
        return GameState(horizontal_lines=self.h_lines, vertical_lines=self.v_lines, points=self.points,
                         boxes=self.boxes)
