import os
from pathlib import Path
import sys

from PySide2 import  QtWidgets, QtCore,QtGui
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import *
from PySide2.QtCore import *
from math import floor
from src.Game import *
from src.Engine import *

class Pong2d(QWidget):
  boardx=50
  boardy=50
  ball=None
  paddles=[None,None]
  player_labels=[None,None]
  firstpress=False
  timer=None
  players_move=[2,2]
  engines=[None,None]
  icons=["pics/ball2.png","pics/paddle.png"]

  def __init__(self,left_isBot,Right_isBot):
    super().__init__()
    self.move(400,200)
    self.resize(700, 400)
    self.game=Game(600,300,"mortimer","blake",left_isBot,Right_isBot)
    if left_isBot:
      self.engines[0]=RiEngine(self.game.players[0].name, self.game.players[0].side, self.game.players[0].paddle,True)
    if Right_isBot:
      self.engines[1]=RiEngine(self.game.players[1].name, self.game.players[1].side, self.game.players[1].paddle,True)
    self.keylist=[]
    self.setupUI()
    

  def getRelativePositionX(self,x):
    return self.boardx + self.game.board_width/2 +x
  
  def getRelativePositionY(self,y):
    return self.boardy +self.game.board_height/2 -y

  def setupUI(self):
    self.ball=QLabel(self)
    self.ball.setPixmap(QPixmap(self.icons[0]))
    self.ball.setScaledContents(True)
    x=self.getRelativePositionX(0)+self.game.ball.diameter/2
    y=self.getRelativePositionY(0)-self.game.ball.diameter/2
    self.ball.setGeometry(QRect(x,y, self.game.ball.diameter, self.game.ball.diameter))

    self.paddles[1]=QLabel(self)
    self.paddles[1].setPixmap(QPixmap(self.icons[1]))
    self.paddles[1].setScaledContents(True)
    x=self.getRelativePositionX(self.game.players[1].paddle.position[0])+self.game.players[1].paddle.thickness/2
    y=self.getRelativePositionY(self.game.players[1].paddle.position[1])-self.game.players[1].paddle.height/2
    self.paddles[1].setGeometry(QRect(x,y, self.game.players[1].paddle.thickness, self.game.players[1].paddle.height))

    self.paddles[0]=QLabel(self)
    self.paddles[0].setPixmap(QPixmap(self.icons[1]))
    self.paddles[0].setScaledContents(True)
    x=self.getRelativePositionX(self.game.players[0].paddle.position[0])+self.game.players[0].paddle.thickness/2
    y=self.getRelativePositionY(self.game.players[0].paddle.position[1])-self.game.players[0].paddle.height/2
    self.paddles[0].setGeometry(QRect(x,y , self.game.players[0].paddle.thickness, self.game.players[0].paddle.height))    

    self.player_labels[1]=QLabel(self)
    self.player_labels[1].setText(self.game.players[1].name+":  "+str(self.game.players[1].points))
    self.player_labels[1].setGeometry(QRect(500,0,200,50))

    self.player_labels[0]=QLabel(self)
    self.player_labels[0].setText(self.game.players[0].name+":  "+str(self.game.players[0].points))
    self.player_labels[0].setGeometry(QRect(100,0,200,50))

    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.updateUi)
    self.timer.start(20) #ms

  def getEngineMove(self,side):
    state=self.game.getState(side)
    statep=(state[2],state[3],state[4],state[5]) #comment this line if the engine is the BFEngine!
    action=self.engines[side].getAction(statep) # up:0, down:1, nothing:2
    return action
  
  def updateUi(self):
    #print("updateui")
    self.game.nextGameStep()
    x=self.getRelativePositionX(self.game.ball.position[0])+self.game.ball.diameter/2
    y=self.getRelativePositionY(self.game.ball.position[1])-self.game.ball.diameter/2
    self.ball.move(x,y)

    #here goes paddle moves-----
    for side in range(2):
      if self.engines[side] !=None:
        move=self.getEngineMove(side)
        #print(move)
        self.game.players[side].movePaddle( move,self.game.board_height)
      else:
        self.game.players[side].movePaddle( self.players_move[side],self.game.board_height)
        self.players_move[side]=2
    
    for i in range(2):
      x=self.getRelativePositionX(self.game.players[i].paddle.position[0])+self.game.players[i].paddle.thickness/2
      y=self.getRelativePositionY(self.game.players[i].paddle.position[1])-self.game.players[i].paddle.height/2
      self.paddles[i].move(x,y)

      txt=self.game.players[i].name+":  "+str(self.game.players[i].points)
      self.player_labels[i].setText(txt)
    self.update()

  def setMove(self):
    for key in self.keylist:
      if key==Qt.Key_Up:
        self.players_move[1]=0
        #print("up")
      if key==Qt.Key_Down:
        self.players_move[1]=1
      if key==Qt.Key_W:
        self.players_move[0]=0
      if key==Qt.Key_S:
        self.players_move[0]=1

  def keyPressEvent(self, event):
    key=event.key()
    self.keylist.append(key)
    self.setMove()


  def keyReleaseEvent(self, event):
    if len(self.keylist)>0:
      del self.keylist[-1]

  def paintEvent(self, e):
    qp = QPainter()
    qp.begin(self)
    qp.setBrush(QColor(100, 150, 150))
    qp.drawRect(self.boardx, self.boardy, self.game.board_width, self.game.board_height)
    qp.end()