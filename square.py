from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QPushButton


class Square(QPushButton):

    left_click = pyqtSignal()
    square_revealed = pyqtSignal()
    flag = pyqtSignal()

    def __init__(self, mine=False, neighbor_mines=0, hidden=True, flag=False):
        super().__init__()

        self.is_mine = mine
        self.neighbor_mines = neighbor_mines
        self.is_hidden = hidden
        self.flagged = flag
        

    def reveal(self):
        self.is_hidden = False
        self.square_revealed.emit()
        
    def set_mine(self):
        self.is_mine = True
        
    def inc_neighbor_mines(self):
        self.neighbor_mines += 1

    def change_flagged_state(self):
        self.flagged = not self.flagged


    def mousePressEvent(self, e):
        if (e.button()==Qt.LeftButton and self.is_hidden and not self.flagged):
            self.left_click.emit()
        elif (e.button()==Qt.RightButton and self.is_hidden):
            self.change_flagged_state()
            self.flag.emit()
            
    
    # TODO: Delete later
    def __str__(self):
        return 'X={0}, Y={1} and hidden={2}'.format(self.is_mine,
                                                    self.neighbor_mines,
                                                    self.is_hidden)