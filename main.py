import random
from time import sleep

from models.board import Board
from models.player import Player
from players.gpt_best_player import AdvancedPlayer
from players.gpt_medium_player import WinningPlayer
from players.player_yaara import SmartPlayer

BOARD_SIZE = 5
POINT_DISTANCE = 120
POINT_SIZE = 8
X_OFFSET = 350
Y_OFFSET = 70
TIMEOUT = 0.3

player1 = SmartPlayer('yaara', 'red')
player2 = AdvancedPlayer('shachar', 'green')


def game_loop(board: Board):
    running = True
    while running:
        board.set_line(*board.current_player.action(board.get_game_state()))
        sleep(TIMEOUT)
        board.get_root().update()
        running = board.check_game_over()
    board.get_root().destroy()


def main():
    board = Board(BOARD_SIZE, POINT_DISTANCE, X_OFFSET,Y_OFFSET, POINT_SIZE, player1, player2)
    game_loop(board)
    board.start_game()


if __name__ == '__main__':
    main()
