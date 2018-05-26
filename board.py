import random
import math

class Square():
    
    def __init__(self, mine = False, neighbor_mines = 0, hidden = True):
        self.is_mine        = mine
        self.neighbor_mines = neighbor_mines
        self.is_hidden      = hidden
        
    def reveal(self):
        self.is_hidden = False
        
    def set_mine(self):
        self.is_mine = True
        
    def inc_neighbor_mines(self):
        self.neighbor_mines += 1

# TODO: Attributes and functions non-public
# La clase *Board* genera un tablero de casillas dados los siguientes parámetros de entrada:
#
#    - width: Anchura del tablero (número de casillas).
#    - height: Altura del tablero (número de casillas).
#    - num_mines: Número de minas que contendrá el tablero.

class Board():
    
    NEIGHBOR_COORDS = (
        (-1, 1), (0, 1), (1, 1),
        (-1, 0),         (1, 0),
        (-1,-1), (0,-1), (1,-1)
    )
    
    def __init__(self, width, height, num_mines):
        self.size_x = width
        self.size_y = height
        self.squares = [[Square() for y in range(self.size_y)] for x in range(self.size_x)]
        
        self.place_mines(num_mines)
    
    def place_mines(self, num_mines):
        mines = random.sample(range(self.size_x * self.size_y), num_mines)
        for i in mines:
            mine_coords = self.get_coordinates(i)
            x = mine_coords[0]
            y = mine_coords[1]
            square = self.squares[x][y]
            square.set_mine()
            
            self.update_neighbors(x, y)
            
    # Example with 3x3 board:
    #     - Mine 0 (mine = 0) belong to the coordinates (0,2). Top-left corner.
    #     - Mine 8 (mine = 8) belong to the coordinates (2,0). Bottom-right corner.
    def get_coordinates(self, mine):
        y = math.floor(mine/self.size_x)
        x = mine - self.size_x*y
        return (x, y)
    
    def update_neighbors(self, coord_x, coord_y):
        for i in range(8):
            x = coord_x + self.NEIGHBOR_COORDS[i][0]
            y = coord_y + self.NEIGHBOR_COORDS[i][1]
            if not (self.invalid_coords(x, y)):
                neighbor = self.squares[x][y]
                neighbor.inc_neighbor_mines()
                
    def invalid_coords(self, coord_x, coord_y):
        return (coord_x < 0 
                or coord_x >= self.size_x 
                or coord_y < 0 
                or coord_y >= self.size_y
        )
    
    # Defined for debugging
    def print_revealed(self):
        res = ''
        
        for y in range(self.size_y):
            for x in range(self.size_x):
                square = self.squares[x][y]
                res += '* ' if square.is_mine else '{} '.format(square.neighbor_mines)
            res += '\n'
        
        return res

#    This function only reveals the selected square. Need to implement a
#    recursive algorithm to reveal contiguous squares without mines.
#
#    def reveal(self, coord_x, coord_y):
#        square = self.squares[coord_x][coord_y]
#        if square.is_mine:
#            print('GAME OVER\n=================')
#            print(self.print_revealed())
#        else:
#            square.reveal()
#            print(self.__str__())
    
    def __str__(self):
        res = ''
        
        for y in range(self.size_y):
            for x in range(self.size_x):
                square = self.squares[x][y]
                res += '_ ' if square.is_hidden else '{} '.format(square.neighbor_mines)
            res += '\n'
        
        return res