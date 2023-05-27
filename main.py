from models import Board

BOARD_SIZE = 10
POINT_DISTANCE = 30
OFFSET = 100

if __name__ == '__main__':
    board = Board(BOARD_SIZE, POINT_DISTANCE, OFFSET)
    board.set_line(5, 3, 5, 4)  # 3, 5
    board.set_line(4, 3, 4, 4)  # 3, 4
    board.set_line(5, 4, 4, 4)  # 4, 4
    board.set_line(5, 3, 4, 3)  # 3, 4
    board.start_game()
