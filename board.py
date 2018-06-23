import random
import math
import operator

from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QObject, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLayout, 
                             QHBoxLayout, QPushButton, QWidget, QGridLayout,
                             QLabel, QStatusBar, QFrame, QDockWidget)

import square as sq
import variable_elimination as ve
import bayesian_network as bn


# Cada dupla corresponde a los valores que hay que sumar
# a una posición determinada del tablero para calcular uno
# de sus 8 posibles vecinos.
NEIGHBOR_POSITION = (
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
)

SQUARE_SIZE = QSize(22, 22)

IMAGE_ICON = 'images/icon(32).png'
IMAGE_MINE = 'images/mina(32).png'
IMAGE_FLAG = 'images/flag.png'
 

# La casilla (0,0) corresponde a la esquina superior izquierda
# Representación de posición: (i,j) ==> i: fila, j: columna
class Board(QMainWindow):

    def __init__(self, height, width, num_of_mines):
        super().__init__()

        self.height = height
        self.width = width
        self.num_of_mines = num_of_mines
        self.evidences = {}
        self.variable_elimination = ve.VariableElimination(
            bn.generateBN(height, width, num_of_mines))

        self.initUi()
        self.place_mines()

    def init_squares(self):
        for i in range(self.height):
            for j in range(self.width):
                square = sq.Square()
                square.setProperty('i', i)
                square.setProperty('j', j)
                square.setFixedSize(SQUARE_SIZE)
                square.left_click.connect(self.handle_left_click)
                square.square_revealed.connect(self.display_square)
                square.flag.connect(self.handle_flag)
                
                self.squares.addWidget(square, i, j)

    def initUi(self):
        self.squares = QGridLayout()
        self.squares.setSpacing(0)
        self.squares.setSizeConstraint(QLayout.SetFixedSize)
        self.init_squares()

        self.game_mine_count = self.num_of_mines
        self.label_mine_count = QLabel('Contador de minas: {0}/{1}'
                              .format(self.game_mine_count, self.num_of_mines))

        hor_bot_box = QHBoxLayout()
        hor_bot_box.addLayout(self.squares)
        
        vert_box = QVBoxLayout()
        vert_box.addLayout(hor_bot_box)

        main_widget = QWidget()
        main_widget.setLayout(vert_box)

        status_bar = QStatusBar()
        status_bar.addWidget(self.label_mine_count)

        self.setCentralWidget(main_widget)
        self.setStatusBar(status_bar)
        self.setWindowTitle('Buscaminas')
        self.setWindowIcon(QtGui.QIcon(IMAGE_ICON))
        self.show()

    def handle_left_click(self):
        square = self.sender()
        self.reveal(square.property('i'), square.property('j'))

    def display_square(self):
        square = self.sender()
        square.setFlat(True)
        square.setEnabled(False)
        square.setStyleSheet('color: black')   

        if square.is_mine:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(IMAGE_MINE), QtGui.QIcon.Disabled)
            square.setIcon(icon)
        elif square.neighbor_mines != 0:
            square.setText(str(square.neighbor_mines))

    def handle_flag(self):
        square = self.sender()
        if square.flagged:
            self.game_mine_count -= 1
            square.setIcon(QtGui.QIcon(IMAGE_FLAG))
            self.label_mine_count.setText('Contador de minas: {0}/{1}'
                              .format(self.game_mine_count, self.num_of_mines))
        else:
            self.game_mine_count += 1
            square.setIcon(QtGui.QIcon())
            self.label_mine_count.setText('Contador de minas: {0}/{1}'
                              .format(self.game_mine_count, self.num_of_mines))

    def get_square(self, i, j):
        return self.squares.itemAtPosition(i, j).widget()
        
    # Coloca las minas en el tablero:
    #   1.- Se genera un número aleatorio distinto
    #       por cada mina.
    #   2.- A cada número aleatorio se le asocia una casilla
    #       mediante "get_position()".
    #   3.- Se coloca cada mina en la posición calculada.
    #   4.- Se actualiza "Square::neighbor_mines" de las
    #       casillas vecinas de cada una de las minas
    #       (llamando a "update_neighbors()").
    
    def place_mines(self):
        num_of_squares = self.width * self.height
        mines = random.sample(range(num_of_squares), self.num_of_mines)
        
        for m in mines:
            mine_position = self.get_position(m)
            i = mine_position[0]
            j = mine_position[1]
            
            self.get_square(i, j).set_mine()
            
            self.update_neighbors(i, j)
    
    # Devuelve la posición (i,j) dado un índice "index":
    #                 
    # +---+---+      Ejemplos con tablero 2x2:
    # | 0 | 1 |
    # +---+---+        - index = 0 ==> (0,0)
    # | 2 | 3 |        - index = 2 ==> (1,0)
    # +---+---+
    def get_position(self, index):
        i = math.floor(index/self.width)
        j = index - self.width*i
        
        return (i, j)
    
    def update_neighbors(self, i, j):
        for n in range(8):
            ni = i + NEIGHBOR_POSITION[n][0]
            nj = j + NEIGHBOR_POSITION[n][1]
            if not (self.invalid_position(ni, nj)):
                self.get_square(ni, nj).inc_neighbor_mines()
    
    # Tiene en cuenta los límites del tablero
    def invalid_position(self, i, j):
        return (j < 0 
                or j >= self.width 
                or i < 0 
                or i >= self.height
               )
               
    def reveal(self, i, j):
        square = self.get_square(i, j)
    
        if square.is_mine:
            print('GAME OVER\n=================')
            print(self.print_revealed())
            return False
        else:
            self.reveal_information(i, j)
            print(self.__str__())
                
        if self.is_end_game():
            print('Congratulations!! \n Victory')
            print(self.print_revealed())
            return False
        else:
            (i, j) = self.suggest_next_square()
            return (i, j)
            
    # P=(i,j): casilla que se encuentra en las coordenadas (i,j)
    # del tablero. Debe mostrar la información de aquellas
    # casillas vecinas hasta que se topa con una cuya Y>=1
    # Flood fill algorithm: https://en.wikipedia.org/wiki/Flood_fill
    def reveal_information(self, i, j):
        if not (self.invalid_position(i, j)):        
            square = self.get_square(i, j)
            if square.is_mine==False and square.is_hidden==True:
                square.reveal()
                self.add_evidence(i, j)
                if square.neighbor_mines==0:
                    for n in range(8):
                        ni = i + NEIGHBOR_POSITION[n][0]
                        nj = j + NEIGHBOR_POSITION[n][1]
                        self.reveal_information(ni, nj)
                
    def suggest_next_square(self):
        prob_X = {}
        hidden = self.get_hidden_squares()
        
        for sq in hidden:
            i = sq[0]
            j = sq[1]
            prob_X[(i, j)] = bn.calcule_prob_X(self.variable_elimination, i, j, 
                                               self.evidences)
        
        # DEBUGGING: print(prob_X)
        # En caso de que haya dos valores máximos, 
        # asigna el primero que encontró
        suggested = max(prob_X.items(), key=operator.itemgetter(1))[0]
        
        # DEBUGGING print('Suggested next square: {}'.format(suggested))
        return suggested
            
    def add_evidence(self, i, j):
        square = self.get_square(i, j)
        X = bn.bn_X_name(i, j)
        Y = bn.bn_Y_name(i, j)
        
        self.evidences[X] = int(square.is_mine)
        self.evidences[Y] = square.neighbor_mines
        # DEBUGGING: print('=============================\n{}\n============================='.format(self.evidences))
    
    def get_hidden_squares(self):
        hidden = set()
        
        for j in range(self.width):
            for i in range(self.height):
                square = self.get_square(i, j)
                if square.is_hidden:
                    hidden.add((i,j))
                    
        return hidden
        
    def is_end_game(self):
        revealed_square_count = len(self.evidences)/2
        board_len = self.width*self.height
        
        return revealed_square_count == board_len - self.num_of_mines
        
    # TODO: Imprime tanto en interfaz gráfica como en consola.
    def print_revealed(self):
        res = ''
        
        for i in range(self.height):
            for j in range(self.width):
                square = self.get_square(i, j)
                square.reveal()
                if square.is_mine:
                    res += '* '
                else:
                    res += '{} '.format(square.neighbor_mines)
            res += '\n'
        
        return res
        
        
    def play_game(self):
        # Al principio de la partida, todas las casillas tienen
        # las mismas posibilidades de contener una mina. Por tanto,
        # el algoritmo debe despejar una cualquiera (ej. (0, 0))
        i = 0
        j = 0
        
        print(self.__str__())
        
        # Se ejecuta recursivamente self.reveal(i, j) 
        # hasta que termina la partida
        next_square = self.reveal(i, j)
        while(next_square):
            i = next_square[0]
            j = next_square[1]
            next_square = self.reveal(i, j)
            
    # DEBUGGING
    def showSelectedSquare(self, i, j):
        square = self.get_square(i, j)
        
        print(square)
        
        
    def __str__(self):
        res = ''
        
        for i in range(self.height):
            for j in range(self.width):
                square = self.get_square(i, j)
                if square.is_hidden:
                    res += '_ '
                else:
                    res += '{} '.format(square.neighbor_mines)
            res += '\n'
        
        return res    