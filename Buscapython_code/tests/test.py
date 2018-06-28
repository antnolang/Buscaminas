import sys
import time

from PyQt5.QtWidgets import QApplication

from src import board as b

def average_time(height, width, num_of_mines):
    app = QApplication(sys.argv)

    count = 0
    ac = 0

    while(count < 20):
        board = b.Board(height, width, num_of_mines)
        start = time.time()
        board.play_game()
        end = time.time()

        if board.is_end_game():
            count += 1
            exe_time = end - start
            ac += exe_time

    print('Media de tiempo de ejecución: {0} seg'.format(ac/count))
    sys.exit()


def average_success(height, width, num_of_mines):
    app = QApplication(sys.argv)

    victory_count = 0
    loss_count = 0
    count = 0

    while(count < 5):
        count += 1
        board = b.Board(height, width, num_of_mines)
        start = time.time()
        board.play_game()
        end = time.time()

        if board.is_end_game():
            victory_count += 1
        else:
            loss_count += 1

    print('- Victorias: {0} de {1}'.format(victory_count, count))
    print('- Derrotas: {0} de {1}'.format(loss_count, count))
    print('- Porcentaje de victoria: {0}'.format(victory_count/count)) 
    sys.exit()