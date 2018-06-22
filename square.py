class Square():
    
    def __init__(self, mine=False, neighbor_mines=0, hidden=True):
        self.is_mine = mine
        self.neighbor_mines = neighbor_mines
        self.is_hidden = hidden
        
    def reveal(self):
        self.is_hidden = False
        
    def set_mine(self):
        self.is_mine = True
        
    def inc_neighbor_mines(self):
        self.neighbor_mines += 1
    
    # Delete later
    def __str__(self):
        return 'X={0}, Y={1} and hidden={2}'.format(self.is_mine,
                                                    self.neighbor_mines,
                                                    self.is_hidden)