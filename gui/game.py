import sys
import math

from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QObject
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGridLayout, QGroupBox, 
                             QPushButton, QDialog, QLayout, QVBoxLayout, 
                             QHBoxLayout, QLabel, QMessageBox)

SQUARE_SIZE = QSize(22, 22)

class Game(QDialog):
    # TODO: En la versión final, solo se pasa board con un objeto Board.
    def __init__(self, board, height, width):
        super().__init__()

        self.board = board
        self.height = height
        self.width = width

        self.initUi()

    def initUi(self):
        # TODO: inicializar cabecera

        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setSizeConstraint(QLayout.SetFixedSize)
        self.init_grid()

        self.hor_top_box = QHBoxLayout()
        # TODO: self.hor_top_box.add(cabecera)

        self.hor_bot_box = QHBoxLayout()
        self.hor_bot_box.addLayout(self.grid)
        
        self.vert_box = QVBoxLayout()
        # TODO: self.vert_box.addLayout(self.hor_top_box)
        self.vert_box.addLayout(self.hor_bot_box)
        
        self.setLayout(self.vert_box)
        self.setWindowTitle("Buscaminas")
        self.setGeometry(100, 100, 680, 500)
        self.setWindowIcon(QtGui.QIcon("images/icon(32).png"))
        self.show()

    def init_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                square = QPushButton('')
                square.setFixedSize(SQUARE_SIZE)
                square.setProperty('i', i)
                square.setProperty('j', j)
                square.clicked.connect(self.reveal_square)
                
                self.grid.addWidget(square, i, j)

    def reveal_square(self):
        hidden_sq = self.sender()
        i = hidden_sq.property('i')
        j = hidden_sq.property('j')
        num_of_neighbors = self.board[i][j]

        pixmap = QtGui.QPixmap('images/{}.png'.format(num_of_neighbors))
        revealed_sq = QLabel()
        revealed_sq.setPixmap(pixmap)
        revealed_sq.setFixedSize(SQUARE_SIZE)
        
        self.grid.replaceWidget(hidden_sq, revealed_sq)
        hidden_sq.setParent(None)
        hidden_sq.deleteLater()