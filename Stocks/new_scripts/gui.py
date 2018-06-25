from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QCheckBox,  QApplication, QWidget, QSizePolicy, QPushButton, QAction, QLineEdit, QMessageBox, QInputDialog, QLabel
from PyQt5.QtGui import *  
from PyQt5.QtCore import QSize 
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys
import os
import random
import pandas as pd
import datetime as dt

from functions import create_bollinger,daily_close

def Start():
    m = App()
    m.show()
    return m

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Patented Amazing Stock Plotting Program'
        self.left = 0
        self.top = 50
        self.width = 1920
        self.height = 1080
        self.initUI()
 
    def initUI(self):
        
        '''Sets up the GUI'''
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        #Stock Symbol Label
        label=QLabel('Stock Symbol:',self)
        label.move(20,25)
        
        #Textbox for Stock Symbol
        self.ticker = QLineEdit(self,text='TSLA')
        self.ticker.move(540,20)
        self.ticker.resize(280,40)
        
        #CheckBox
        self.b1 = QCheckBox("Bolinger Bands",self)
        self.b1.move(860,20)
        self.b1.resize(320,40)
        
        self.b2 = QCheckBox("Optimal Simple Moving Averages",self)
        self.b2.move(860,60)
        self.b2.resize(320,40)
        
        self.b3 = QCheckBox("P/E Ratio",self)
        self.b3.move(860,100)
        self.b3.resize(320,40)
        
        self.b4 = QCheckBox("Oscillator",self)
        self.b4.move(860,140)
        self.b4.resize(320,40)

        # Create a quit buttom
        self.button = QPushButton('Quit',self)
        self.button.move(860,200)
        self.button.clicked.connect(self.exiting)
        
        
        self.button = QPushButton('Plot',self)
        self.button.move(540,200)
        self.button.clicked.connect(self.start_plot)
 
                
    def start_plot(self):
        '''Feeds the PlotCanvas the variables it needs and shows a plot'''
        m = PlotCanvas(self,ticker=self.ticker.text())
        m.move(0,0)
        
    def exiting(self):
        sys.exit()
        
        
        
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100,ticker='TSLA'):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ticker = ticker
        self.plot()
 
 
    def plot(self):
        
        location=os.path.expanduser('~/Documents/daily_close')
            
        curr = dt.datetime.now().date()
        start = curr-dt.timedelta(days=365)
        
        daily_close(self.ticker,location=location,start=start)
        
        data = pd.read_csv('{}/{}.csv'.format(location,self.ticker))
        
        ax = self.figure.add_subplot(111)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.plot(data['close'],'k--',alpha=.6)
        ax.set_xticks([0,len(data['close'])/4,len(data['close'])/2,\
                       3*len(data['close'])/4,len(data['close'])])
        ax.set_xticklabels([start,start+dt.timedelta(days=int(len(\
data['close'])/4)),start+dt.timedelta(days=int(len(data['close'])/2)),start+dt\
    .timedelta(days=int(3*len(data['close'])/4)),curr],rotation=45)
        ax.set_title('PyQt Matplotlib Example')
        self.draw()
        self.show()

        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Start()
    app.exec_()