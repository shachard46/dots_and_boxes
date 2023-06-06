import random
from time import sleep

from game_blocks.board import Board
from game_blocks.player import Player
from players.gpt_best_player import AdvancedPlayer
from players.gpt_medium_player import WinningPlayer
from players.player_yaara import RandomPlayer, SmartRandomPlayer, VerySmartRandomPlayer

BOARD_SIZE = 6
POINT_DISTANCE = 100
POINT_SIZE = 8
X_OFFSET = 350
Y_OFFSET = 70
TIMEOUT = 0.3

player1 = VerySmartRandomPlayer('yaara', 'red')
player2 = RandomPlayer('shachar', 'green')


def game_loop(board: Board):
    running = True
    while running:
        board.set_line(*board.current_player.action(board.get_game_state()))
        sleep(TIMEOUT)
        board.get_root().update()
        running = board.check_game_over()
    board.get_root().destroy()


def main():
    board = Board(BOARD_SIZE, POINT_DISTANCE, X_OFFSET, Y_OFFSET, POINT_SIZE, player1, player2)
    game_loop(board)
    board.start_game()


if __name__ == '__main__':
    main()
