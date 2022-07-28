import random
from math import sin,cos,pi,sqrt

class Ball:
  diameter=15
  step_size=0
  position=None
  step=None

  def __init__(self,position,step):
    self.position=position
    self.step=step
    self.step_size=sqrt(step[0]**2+step[1]**2)

  def moveOneStep(self):
    self.position[0]+=self.step[0]
    self.position[1]+=self.step[1]
    #print(position)
  
  def reverseUpDown(self):
    self.step[1]=-self.step[1]
  
  def reverseLeftRight(self,alpha,side):
    self.step[0]=self.step_size*cos(pi+pi*(1-side)+alpha*pi/4)
    self.step[1]=self.step_size*sin(pi+pi*(1-side)+alpha*pi/4)
  
  def resetPosition(self):
    self.position=[0,0]

class Paddle:
  thickness=8
  height=50
  position=None
  step=None
  
  def __init__(self,position,step):
    self.position=position
    self.step=step
  
  def moveUp(self):
    self.position[1]+=self.step
  
  def moveDown(self):
    self.position[1]-=self.step

  def resetPosition(self):
    self.position[1]=0

class Agent:
  name=""
  points=0
  isBot=False
  side=0 # 0: left, 1: right
  paddle=None

  def __init__(self,name,side,paddle,isBot):
    self.isBot=isBot
    if isBot:
      name+="_Bot"
    self.name=name
    self.side=side
    self.paddle=paddle

  def movePaddle(self,action,board_height):
    """
        action= 0: up, 1: down
        side= 0: left, 1: right
    """
    cond1=self.paddle.position[1]+self.paddle.step+self.paddle.height/2<=board_height/2
    cond2=self.paddle.position[1]-self.paddle.step-self.paddle.height/2>=-board_height/2
    if action==0 and cond1:
      self.paddle.moveUp()
    elif action==1 and cond2:
      self.paddle.moveDown()
