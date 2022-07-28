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

class Pong2d(QWidget):
  boardx=50
  boardy=50
  ball=None
  paddles=[None,None]
  player_labels=[None,None]
  firstpress=False
  timer=None
  icons=["pics/ball2.png","pics/paddle.png"]

  def __init__(self):
    super().__init__()
    self.move(400,200)
    self.resize(700, 400)
    self.game=Game(600,300,"mortimer","blake")
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
    self.timer.start(20) #1 min intervall
  
  def updateUi(self):
    #print("updateui")
    self.game.gameLoop()
    x=self.getRelativePositionX(self.game.ball.position[0])+self.game.ball.diameter/2
    y=self.getRelativePositionY(self.game.ball.position[1])-self.game.ball.diameter/2
    self.ball.move(x,y)

    for i in range(2):
      x=self.getRelativePositionX(self.game.players[i].paddle.position[0])+self.game.players[i].paddle.thickness/2
      y=self.getRelativePositionY(self.game.players[i].paddle.position[1])-self.game.players[i].paddle.height/2
      self.paddles[i].move(x,y)

      txt=self.game.players[i].name+":  "+str(self.game.players[i].points)
      self.player_labels[i].setText(txt)


    self.update()

  def makeChanges(self):
    for key in self.keylist:
      if key==Qt.Key_Up:
        self.game.players[1].movePaddle( 0,self.game.board_height)
      elif key==Qt.Key_Down:
        self.game.players[1].movePaddle(1,self.game.board_height)
      elif key==Qt.Key_W:
        self.game.players[0].movePaddle( 0,self.game.board_height)
      elif key==Qt.Key_S:
        self.game.players[0].movePaddle( 1,self.game.board_height)
      
    #self.updateUi()

  def keyPressEvent(self, event):
    key=event.key()
    self.keylist.append(key)
    self.makeChanges()


  def keyReleaseEvent(self, event):
    if len(self.keylist)>0:
      del self.keylist[-1]

  def paintEvent(self, e):
    qp = QPainter()
    qp.begin(self)
    qp.setBrush(QColor(100, 150, 150))
    qp.drawRect(self.boardx, self.boardy, self.game.board_width, self.game.board_height)
    qp.end()

        
##################################################
if __name__ == "__main__":
  import sys
  app = QApplication(sys.argv)
  window = Pong2d()
  #PromotionWindow(500, 150, 0)
  window.show()
  sys.exit(app.exec_())