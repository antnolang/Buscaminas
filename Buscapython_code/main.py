import sys

from PyQt5.QtWidgets import QApplication

from tests.test import average_time
from tests.test import average_success
from src import board as b


def main(height, width, num_of_mines):
    app = QApplication(sys.argv)
    board = b.Board(height, width, num_of_mines)
    sys.exit(app.exec())


if __name__ == '__main__':
    if len(sys.argv) == 4:
        height = sys.argv[1]
        height = int(height.replace('-', ''))
        width = sys.argv[2]
        width = int(width.replace('-', ''))
        num_of_mines = sys.argv[3]
        num_of_mines = int(num_of_mines.replace('-', ''))

        main(height, width, num_of_mines)
    elif len(sys.argv) == 5 and sys.argv[1] == '--testtime':
        height = sys.argv[2]
        height = int(height.replace('-', ''))
        width = sys.argv[3]
        width = int(width.replace('-', ''))
        num_of_mines = sys.argv[4]
        num_of_mines = int(num_of_mines.replace('-', ''))

        average_time(height, width, num_of_mines)
    elif len(sys.argv) == 5 and sys.argv[1] == '--testsuccess':
        height = sys.argv[2]
        height = int(height.replace('-', ''))
        width = sys.argv[3]
        width = int(width.replace('-', ''))
        num_of_mines = sys.argv[4]
        num_of_mines = int(num_of_mines.replace('-', ''))

        average_success(height, width, num_of_mines)
    else:
        main(5, 5, 5)