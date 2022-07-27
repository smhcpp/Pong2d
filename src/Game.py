from src.Board import *

class Game:
    board=None
    hit_turn=0
    right_player=None
    left_player=None
    
    def __init__(self,boardwidth,boardheight,left_player_name,right_player_name):
        self.board=Board(boardwidth, boardheight)
        self.right_player=Agent(right_player_name, 1)
        self.left_player=Agent(left_player_name, 0)