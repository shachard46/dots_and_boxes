import random
from time import sleep

from models import Board
from models.player import Player

BOARD_SIZE = 10
POINT_DISTANCE = 30
OFFSET = 100

player1 = Player(lambda state: (random.randint(0, 9), 4, random.randint(0, 9), 4))
player2 = Player(lambda state: (random.randint(0, 9), 4, random.randint(0, 9), 4))


def game_loop(board: Board):
    running = True
    while running:
        board.set_line(*player1.action(board.get_game_state()))
        sleep(0.5)
        board.set_line(*player2.action(board.get_game_state()))
        sleep(0.5)
        board.root.update()
    board.root.destroy()


def main():
    board = Board(BOARD_SIZE, POINT_DISTANCE, OFFSET)
    game_loop(board)
    board.start_game()


if __name__ == '__main__':
    main()
