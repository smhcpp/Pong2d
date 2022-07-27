from src.Utilites import *

class Board:
  width=500
  height=100
  ball=None
  left_paddle=None
  right_paddle=None
  board_to_paddle_distance=50

  def __init__(self,width,height):
    self.width=width
    self.height=height
    self.setup()

  def setup(self):
    self.ball=Ball((0,0), (0,0))
    posx=self.width/2-self.board_to_paddle_distance
    self.left_paddle=Paddle((-posx,0), (0,0))
    self.right_paddle=Paddle((posx,0), (0,0))
  