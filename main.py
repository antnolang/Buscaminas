import sys

from PyQt5.QtWidgets import QApplication

from tests.test_time import average_time
import board as b


def main(height, width, num_of_mines):
    app = QApplication(sys.argv)
    board = b.Board(height, width, num_of_mines)
    sys.exit(app.exec())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        height = sys.argv[2]
        height = int(height.replace('-', ''))
        width = sys.argv[3]
        width = int(width.replace('-', ''))
        num_of_mines = sys.argv[4]
        num_of_mines = int(num_of_mines.replace('-', ''))

        if sys.argv[1] == '--testtime':
            average_time(b, width, height, num_of_mines)
        else:
            main(width, height, num_of_mines)
    else:
        main(5, 5, 5)