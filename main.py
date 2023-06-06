import random
from time import sleep

from models.board import Board
from models.player import Player

BOARD_SIZE = 10
POINT_DISTANCE = 30
OFFSET = 100

player1 = Player('yaara', 'red')
player2 = Player('shachar', 'green')


def game_loop(board: Board):
    running = True
    while running:
        board.set_line(*player1.action(board.get_game_state()))
        sleep(0.5)
        board.set_line(*player2.action(board.get_game_state()))
        sleep(0.5)
        board.get_root().update()
    board.get_root().destroy()


def main():
    board = Board(BOARD_SIZE, POINT_DISTANCE, OFFSET, [player1.color, player2.color])
    game_loop(board)
    board.start_game()


if __name__ == '__main__':
    main()
