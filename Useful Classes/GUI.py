import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QCheckBox,  QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QInputDialog, QLabel
from PyQt5.QtGui import *  
from PyQt5.QtCore import QSize 

def Start():
    m = GUI()
    m.show()
    return m

class GUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Title'
        self.left = 0
        self.top = 50
        self.width = 840
        self.height = 280
        self.button_count=0
        self.label_count=0
        self.initUI()
        
    def create_label(self,name,column,row):
        
        label=QLabel(str(name),self)
        label.move(20*row,25*column)
        
    def create_button(self,name,column,row),commanding_function=None:
        
        button=QPushButton(str(name),self,command=commanding_function)
        button.move(20*row,25*column)
        
        self.button_count+=1
        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.create_label('thing',1,1)
    
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Start()
    app.exec_()