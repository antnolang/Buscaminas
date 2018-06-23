import sys

from PyQt5.QtWidgets import QApplication

import board as b


def main():
    app = QApplication(sys.argv)
    board = b.Board(5, 5, 5)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()