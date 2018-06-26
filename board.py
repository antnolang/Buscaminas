import random
import math
import operator

from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QLayout, 
                             QPushButton, QWidget, QGridLayout, QLabel,
                             QStatusBar, QAction)

import square as sq
import variable_elimination as ve
import bayesian_network as bn
import additional_windows as aux_windows


# Cada dupla corresponde a los valores que hay que sumar
# a una posición determinada del tablero para calcular uno
# de sus 8 posibles vecinos.
NEIGHBOR_POSITION = (
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
)

SQUARE_SIZE = QSize(24, 24)

IMAGE_ICON = 'images/icon.png'
IMAGE_MINE = 'images/mina.png'
IMAGE_FLAG = 'images/flag.png'

NUMBER_COLORS = ['', 'blue', 'green', 'red', 'blueViolet', 
                 'brown', 'yellow', 'aquamarine', 'black']
 

# La casilla (0,0) corresponde a la esquina superior izquierda
# Representación de posición: (i,j) ==> i: fila, j: columna
class Board(QMainWindow):

    def __init__(self, height, width, num_of_mines):
        super().__init__()

        self.height = height
        self.width = width
        self.num_of_mines = num_of_mines
        self.evidences = {}
        self.suggested_pos = (0, 0)
        self.variable_elimination = ve.VariableElimination(
            bn.generate_BN(height, width, num_of_mines))

        self.initUi()
        self.place_mines()

    def initUi(self):
        # Inicializar la barra del menú
        menu = self.menuBar()
        game_menu = menu.addMenu('Juego')
        help_menu = menu.addMenu('Ayuda')

        new_game_action = QAction('Nueva partida', self)
        new_game_action.setShortcut('Ctrl+N')
        new_game_action.triggered.connect(self.new_game)
        restart_action = QAction('Configurar partida', self)
        restart_action.setShortcut('Ctrl+C')
        restart_action.triggered.connect(self.conf_dialog)
        resolve_action = QAction('Resolver automáticamente', self)
        resolve_action.setShortcut('Ctrl+A')
        resolve_action.triggered.connect(self.play_game)
        game_menu.addAction(new_game_action)
        game_menu.addAction(restart_action)
        game_menu.addAction(resolve_action)

        rules = QAction('Reglas del juego del Buscaminas', self)
        rules.triggered.connect(self.rules_dialog)
        suggest_mechanism = QAction('Mecanismo de sugerencia', self)
        suggest_mechanism.triggered.connect(self.suggest_dialog)
        help_menu.addAction(rules)
        help_menu.addAction(suggest_mechanism)
        
        # Inicializar el tablero de casillas
        self.squares = QGridLayout()
        self.squares.setSpacing(0)
        self.squares.setSizeConstraint(QLayout.SetFixedSize)
        self.init_squares()

        # Inicializar la barra de estado
        self.game_mine_count = self.num_of_mines
        self.label_mine_count = QLabel('Contador de minas: {0}/{1}'
                              .format(self.game_mine_count, self.num_of_mines))

        # Configuración de layouts de la ventana
        hor_bot_box = QHBoxLayout()
        hor_bot_box.addLayout(self.squares)
        
        vert_box = QVBoxLayout()
        vert_box.addLayout(hor_bot_box)

        main_widget = QWidget()
        main_widget.setLayout(vert_box)

        status_bar = QStatusBar()
        status_bar.addWidget(self.label_mine_count)

        # Pasar a QMainWindow los layouts con los elementos inicializados
        self.setCentralWidget(main_widget)
        self.setStatusBar(status_bar)
        self.setMenuBar(menu)

        # Inicialización del resto de atributos de la ventana
        self.setWindowTitle('Buscaminas')
        self.setWindowIcon(QtGui.QIcon(IMAGE_ICON))
        self.show()

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

    def get_square(self, i, j):
        return self.squares.itemAtPosition(i, j).widget()
    
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

    def is_end_game(self):
        revealed_square_count = len(self.evidences)/2
        board_len = self.width*self.height
        
        return revealed_square_count == board_len - self.num_of_mines
               
    def reveal_all_board(self):
        for i in range(self.height):
            for j in range(self.width):
                square = self.get_square(i, j)
                square.reveal()

    def reveal(self, i, j):
        square = self.get_square(i, j)
    
        if square.is_mine:
            self.reveal_all_board()
            end_window = aux_windows.EndGame(False)
            end_window.exec()
            self.suggested_pos = False
        else:
            self.reveal_information(i, j)
                
            if self.is_end_game():
                self.reveal_all_board()
                end_window = aux_windows.EndGame(True)
                end_window.exec()
                self.suggested_pos = False
            else:
                self.suggested_pos = self.suggest_next_square()
            
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

    def add_evidence(self, i, j):
        square = self.get_square(i, j)
        X = bn.bn_X_name(i, j)
        Y = bn.bn_Y_name(i, j)
        
        self.evidences[X] = int(square.is_mine)
        self.evidences[Y] = square.neighbor_mines
        # DEBUGGING: print('=============================\n{}\n============================='.format(self.evidences))
                
    def suggest_next_square(self):
        prob_X = {}
        hidden = self.get_hidden_squares()
        
        for sq in hidden:
            i = sq[0]
            j = sq[1]
            prob_X[(i, j)] = bn.calcule_prob_X(self.variable_elimination, i, j, 
                                               self.evidences)
        
        # DEBUGGING: print(prob_X)

        # Primera casilla con mayor probabilidad
        # de no contener una mina.
        return max(prob_X.items(), key=operator.itemgetter(1))[0]
    
    def get_hidden_squares(self):
        hidden = set()
        
        for j in range(self.width):
            for i in range(self.height):
                square = self.get_square(i, j)
                if square.is_hidden:
                    hidden.add((i,j))
                    
        return hidden
        
    def __str__(self):
        res = ''
        
        for i in range(self.height):
            for j in range(self.width):
                square = self.get_square(i, j)
                if square.is_hidden:
                    res += '_ '
                elif square.is_mine:
                    res += '* '
                else:
                    res += '{} '.format(square.neighbor_mines)
            res += '\n'
        
        return res    


    # Las siguientes funciones corresponden a los "slots" de Board():
    def play_game(self):
        if self.suggested_pos:
            print('Pasos de la resolución automática:\n')
            while(self.suggested_pos):
                i = self.suggested_pos[0]
                j = self.suggested_pos[1]
                self.reveal(i, j)
                print('{0}\nCasilla seleccionada: {1}\n'.format(self, (i, j)))
                print('============================')

            if self.get_square(i, j).is_mine:
                print('\tDERROTA\n=============================')
            else:
                print('\tVICTORIA\n=============================')

    def handle_left_click(self):
        i = self.suggested_pos[0]
        j = self.suggested_pos[1]
        self.get_square(i, j).setStyleSheet('')

        square = self.sender()
        self.reveal(square.property('i'), square.property('j'))
        
        if self.suggested_pos:
            i = self.suggested_pos[0]
            j = self.suggested_pos[1]
            self.get_square(i, j).setStyleSheet('background-color: green')

    def display_square(self):
        square = self.sender()
        square.setFlat(True)
        square.setEnabled(False) 

        if square.is_mine:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(IMAGE_MINE), QtGui.QIcon.Disabled)
            square.setIcon(icon)
        elif square.neighbor_mines != 0:
            square.setText(str(square.neighbor_mines))
            square.setStyleSheet('font-weight: bold; color: {0};'
                                 .format(NUMBER_COLORS[square.neighbor_mines]))

    def handle_flag(self):
        square = self.sender()
        if not square.flagged and not self.game_mine_count == 0:
            square.change_flagged_state()
            square.setIcon(QtGui.QIcon(IMAGE_FLAG))
            self.game_mine_count -= 1
            self.label_mine_count.setText('Contador de minas: {0}/{1}'
                              .format(self.game_mine_count, self.num_of_mines))
        elif square.flagged:
            square.change_flagged_state()
            square.setIcon(QtGui.QIcon())
            self.game_mine_count += 1
            self.label_mine_count.setText('Contador de minas: {0}/{1}'
                              .format(self.game_mine_count, self.num_of_mines))

    def new_game(self):
        self.close()
        self.__init__(self.height, self.width, self.num_of_mines)

    def conf_dialog(self):
        conf_window = aux_windows.Configuration(self)
        conf_window.exec()

    def rules_dialog(self):
        help_window = aux_windows.HelpRules()
        help_window.exec()

    def suggest_dialog(self):
        suggest_window = aux_windows.HelpSuggestion()
        suggest_window.exec()