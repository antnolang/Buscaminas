import sys

from PyQt5.QtWidgets import QApplication
from gui.game import Game

BOARD = [[0, 1, 2, 2, 1],
         [0, 1, 9, 9, 2],
         [1, 2, 2, 3, 9],
         [9, 2, 1, 2, 1],
         [1, 2, 9, 1, 0]] 
WIDTH = 5
HEIGHT = 5
NUM_OF_MINES = 5

# TODO: def main // __name__ ?
app = QApplication(sys.argv)
game = Game(BOARD, HEIGHT, WIDTH)
sys.exit(app.exec())