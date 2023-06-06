from typing import Tuple, List, Union

from game_blocks.game_state import GameState
from game_blocks.shapes import Point, Line, Box


class AdvancedPlayer:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def action(self, game_state: GameState) -> Tuple[int, int, int, int]:
        best_move = None
        best_score = float('-inf')

        for row in range(len(game_state.lines)):
            for col in range(len(game_state.lines[row])):
                line_pair = game_state.lines[row][col]

                # Check horizontal line
                if line_pair[0] is None and line_pair[1] is None:
                    score = self.evaluate_move(game_state, row, col, True)
                    if score > best_score:
                        best_move = (row, col, True)
                        best_score = score

                # Check vertical line
                if line_pair[0] is None and line_pair[1] is None:
                    score = self.evaluate_move(game_state, row, col, False)
                    if score > best_score:
                        best_move = (row, col, False)
                        best_score = score

        if best_move is not None:
            move_row, move_col, is_horizontal = best_move
            line = Line(game_state.points[move_row][move_col],
                        game_state.points[move_row + is_horizontal][move_col + (not is_horizontal)],
                        self.color, None)
            x1, y1 = line.p1.x, line.p1.y
            x2, y2 = line.p2.x, line.p2.y
            return x1, y1, x2, y2
        else:
            return 0, 0, 0, 0

    def evaluate_move(self, game_state: GameState, row: int, col: int, is_horizontal: bool) -> float:
        temp_points = [point.copy() for point in game_state.points]
        temp_lines = [[line.copy() if line else None for line in row] for row in game_state.lines]
        temp_boxes = [[box.copy() if box else None for box in row] for row in game_state.boxes]
        temp_game_state = GameState(temp_points, temp_lines, temp_boxes)

        temp_game_state.lines[row][col][0] = Line(temp_game_state.points[row][col],
                                                  temp_game_state.points[row + is_horizontal][
                                                      col + (not is_horizontal)],
                                                  self.color, None)

        completed_boxes = self.get_completed_boxes(temp_game_state, row, col, is_horizontal)
        score = len(completed_boxes) * 10

        for box in completed_boxes:
            opponent_moves = self.get_possible_opponent_moves(temp_game_state, box)
            for move in opponent_moves:
                opponent_row, opponent_col, opponent_is_horizontal = move
                opponent_score = self.evaluate_move(temp_game_state, opponent_row, opponent_col, opponent_is_horizontal)
                score -= opponent_score / len(opponent_moves)

        return score

    def get_completed_boxes(self, game_state: GameState, row: int, col: int, is_horizontal: bool) -> List[Box]:
        completed_boxes = []

        if row > 0 and row < len(game_state.boxes) and col < len(game_state.boxes[row - 1]):
            box = game_state.boxes[row - 1][col]
            if box is not None and box.last_line is None:
                completed_boxes.append(box)

        if row < len(game_state.boxes) and col < len(game_state.boxes[row]):
            box = game_state.boxes[row][col]
            if box is not None and box.last_line is None:
                completed_boxes.append(box)

        return completed_boxes

    def get_possible_opponent_moves(self, game_state: GameState, box: Box) -> List[Tuple[int, int, bool]]:
        possible_moves = []

        for row in range(len(game_state.lines)):
            for col in range(len(game_state.lines[row])):
                line_pair = game_state.lines[row][col]

                if line_pair[0] is None and line_pair[1] is None:
                    temp_game_state = game_state.copy()
                    temp_game_state.lines[row][col][0] = Line(temp_game_state.points[row][col],
                                                              temp_game_state.points[row + 1][col],
                                                              self.color, None)

                    new_boxes = self.get_completed_boxes(temp_game_state, row, col, True)
                    if box in new_boxes:
                        possible_moves.append((row, col, True))

                if line_pair[0] is None and line_pair[1] is None:
                    temp_game_state = game_state.copy()
                    temp_game_state.lines[row][col][1] = Line(temp_game_state.points[row][col],
                                                              temp_game_state.points[row][col + 1],
                                                              self.color, None)

                    new_boxes = self.get_completed_boxes(temp_game_state, row, col, False)
                    if box in new_boxes:
                        possible_moves.append((row, col, False))

        return possible_moves
