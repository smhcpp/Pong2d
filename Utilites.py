class Ball:
  min_speed=30
  max_speed=60
  position=None
  velocity=None
  def __init__(self,position,velocity):
    self.position=position
    self.velocity=velocity
  
  def __init__(self,position,velocity,min_speed,max_speed):
    self.position=position
    self.velocity=velocity
    self.min_speed=min_speed
    self.max_speed=max_speed

class Paddle:
  thickness=10
  position=None
  velocity=None
  
  def __init__(self,position,velocity):
    self.position=position
    self.velocity=velocity

  def __init__(self,position,velocity,thickness):
    self.position=position
    self.velocity=velocity
    self.thickness=thickness

  def hit(self,ball):
    pass
