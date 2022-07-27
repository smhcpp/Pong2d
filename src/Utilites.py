class Ball:
  min_speed=30
  max_speed=60
  radius=15
  position=None
  velocity=None
  def __init__(self,position,velocity):
    self.position=position
    self.velocity=velocity

class Paddle:
  thickness=5
  height=50
  position=None
  velocity=None
  
  def __init__(self,position,velocity):
    self.position=position
    self.velocity=velocity

  def hit(self,ball):
    pass

class Agent:
  name=""
  points=0
  side=0 # 0: left, 1: right
  #paddle=None

  def __init__(self,name,side):
    self.name=name
    self.side=side
 #   self.paddle=paddle
