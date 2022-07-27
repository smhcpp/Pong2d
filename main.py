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
  right_paddle=None
  left_paddle=None
  right_player_label=None
  left_player_label=None
  icons=["pics/ball2.png","pics/paddle.png"]

  def __init__(self):
    super().__init__()
    self.move(300,100)
    self.resize(800, 500)
    self.game=Game(700,400,"mortimer","blake")
    self.setupUI()

  def getRelativePositionX(self,x):
    return self.boardx + self.game.board.width/2 +x
  
  def getRelativePositionY(self,y):
    return self.boardy +self.game.board.height/2 +y

  def setupUI(self):
    self.ball=QLabel(self)
    self.ball.setPixmap(QPixmap(self.icons[0]))
    self.ball.setScaledContents(True)
    x=self.getRelativePositionX(0)+self.game.board.ball.radius
    y=self.getRelativePositionY(0)-self.game.board.ball.radius
    self.ball.setGeometry(QRect(x,y, self.game.board.ball.radius, self.game.board.ball.radius))

    self.right_paddle=QLabel(self)
    self.right_paddle.setPixmap(QPixmap(self.icons[1]))
    self.right_paddle.setScaledContents(True)
    x=self.getRelativePositionX(self.game.board.right_paddle.position[0])+self.game.board.right_paddle.thickness/2
    y=self.getRelativePositionY(self.game.board.right_paddle.position[1])-self.game.board.right_paddle.height/2
    self.right_paddle.setGeometry(QRect(x,y, self.game.board.right_paddle.thickness, self.game.board.right_paddle.height))

    self.left_paddle=QLabel(self)
    self.left_paddle.setPixmap(QPixmap(self.icons[1]))
    self.left_paddle.setScaledContents(True)
    x=self.getRelativePositionX(self.game.board.left_paddle.position[0])+self.game.board.left_paddle.thickness/2
    y=self.getRelativePositionY(self.game.board.left_paddle.position[1])-self.game.board.left_paddle.height/2
    self.left_paddle.setGeometry(QRect(x,y , self.game.board.left_paddle.thickness, self.game.board.left_paddle.height))    

    self.right_player_label=QLabel(self)
    self.right_player_label.setText(self.game.right_player.name+":  "+str(self.game.right_player.points))
    self.right_player_label.setGeometry(QRect(600,0,200,50))

    self.left_player_label=QLabel(self)
    self.left_player_label.setText(self.game.left_player.name+":  "+str(self.game.left_player.points))
    self.left_player_label.setGeometry(QRect(100,0,200,50))

  def paintEvent(self, e):
    qp = QPainter()
    qp.begin(self)
    qp.setBrush(QColor(100, 150, 150))
    qp.drawRect(self.boardx, self.boardy, self.game.board.width, self.game.board.height)
    qp.end()

        
##################################################
if __name__ == "__main__":
  import sys
  app = QApplication(sys.argv)
  window = Pong2d()
  #PromotionWindow(500, 150, 0)
  window.show()
  sys.exit(app.exec_())