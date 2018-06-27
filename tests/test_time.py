import sys
import time

from PyQt5.QtWidgets import QApplication

def average_time(b, height, width, num_of_mines):
    app = QApplication(sys.argv)

    count = 0
    ac = 0

    while(count < 40):
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