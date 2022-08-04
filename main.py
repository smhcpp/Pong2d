import os
from pathlib import Path
import sys

from PySide2 import  QtWidgets, QtCore,QtGui
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import *
from PySide2.QtCore import *
from math import floor
from src.Pong2dGui import *
        
##################################################
if __name__ == "__main__":
  import sys
  app = QApplication(sys.argv)
  window = Pong2d(True,False)
  #PromotionWindow(500, 150, 0)
  window.show()
  sys.exit(app.exec_())