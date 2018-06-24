import sys
import time

from PyQt5.QtWidgets import QApplication

import board as b


def main(height, width, num_of_mines):
    app = QApplication(sys.argv)
    board = b.Board(height, width, num_of_mines)
    sys.exit(app.exec())


if __name__ == '__main__':
    main(5, 5, 5)