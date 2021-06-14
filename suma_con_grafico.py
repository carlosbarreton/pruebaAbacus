import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.Qt import Qt
from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
from time import localtime, strftime
import numpy as np

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.counter = 0

        # Color configs
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # Add title
        self.setWindowTitle("Suma con gráfico")

        # Create some widgets to be placed inside
        self.lblInstruction = QtGui.QLabel('Ingrese un número entre 1 y 5')
        self.btnReset = QtGui.QPushButton('Reiniciar contador')
        self.btnExit = QtGui.QPushButton('Salir')
        self.lblWarning = QtGui.QLabel('')
        self.listw = QtGui.QListWidget()
        self.listw.setWordWrap(True)
        self.graph = pg.PlotWidget()
   
        # Create a grid layout
        self.setLayout(QtGui.QGridLayout())
   
        # Add widgets to the layout 
        self.layout().addWidget(self.lblInstruction, 0, 0, 1, 2)
        self.layout().addWidget(self.btnReset, 1, 0)
        self.layout().addWidget(self.btnExit, 1, 1)
        self.layout().addWidget(self.lblWarning, 2, 0, 1, 2)
        self.layout().addWidget(self.listw, 3, 0, 1, 2)
        self.layout().addWidget(self.graph, 0, 2, 4, 1)

        # Add functionality to GUI elements
        self.listw.setWordWrap(True)
        self.listw.keyPressEvent = self.keyPressEvent
        self.listw.addItem('El usuario inicia la ejecución a las ' + strftime('%H:%M:%S', \
                localtime()))
        self.btnReset.clicked.connect(self.reset_counter)
        self.btnReset.keyPressEvent = self.keyPressEvent
        self.btnExit.clicked.connect(self.close)
        self.btnExit.keyPressEvent = self.keyPressEvent

        # Plot
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)
    
        self.graph.plotItem.setDownsampling(mode='peak')
        self.graph.plotItem.setRange(xRange = [-30,0])
        self.graph.plotItem.setRange(yRange = [0,1.1])
        self.graph.plotItem.setLabel('bottom', text='tiempo', units='s')
        self.graph.plotItem.setLabel('left', text='suma acumulada')
        self.graph.plotItem.showGrid(x=True, y=True)
        self.pen = pg.mkPen(color=(232, 76, 34), width = 5)
        self.curve = self.graph.plotItem.plot(pen = self.pen)
        
        self.validKeyPressed = False
        self.curves = []
        self.chunkSize = 10000
        self.maxChunks = 1000
        self.data = np.empty((self.chunkSize+1,2))
        self.index = 0
        self.startTime = pg.ptime.time()

    def update_plot(self):
        now = pg.ptime.time()
        for c in self.curves:
            c.setPos(-(now-self.startTime),0)

        i = self.index % self.chunkSize
        if i == 0:
            self.curves.append(self.curve)
            last = self.data[-1]
            self.data = np.empty((self.chunkSize+1,2))
            self.data[0] = last
        else:
            self.curve = self.curves[-1]

        self.data[i+1,0] = now - self.startTime
        self.data[i+1,1] = self.counter
        self.curve.setData(x=self.data[:i+2,0], y=self.data[:i+2,1])
        self.index += 1
        
        if self.validKeyPressed and self.counter != 0:
            self.graph.plotItem.setRange(yRange = [0, 1.1*self.counter])

    def keyPressEvent(self, signal):
        keyPressed = signal.key()
        if keyPressed == Qt.Key_1 or keyPressed == Qt.Key_2 or keyPressed == Qt.Key_3 or \
                keyPressed == Qt.Key_4 or keyPressed == Qt.Key_5:
            self.list_event(keyPressed % Qt.Key_1 + 1)
            self.lblWarning.setText('')
            self.validKeyPressed = True
        else:
            self.lblWarning.setStyleSheet("color: red")
            self.lblWarning.setText('Debe ingresar un número entre 1 y 5')

    def list_event(self, number):
        message = 'El usuario oprime la tecla' + ' \'' + str(number) + '\' a las ' + \
                strftime('%H:%M:%S', localtime()) 
        self.counter += number
        self.listw.addItem(message)
        self.listw.scrollToBottom()

    def reset_counter(self):
        if self.validKeyPressed:
            self.graph.plotItem.setRange(yRange = [0,1.1*self.counter])
        self.counter = 0
        message = 'El usuario oprime el botón de \'reinicio de contador\' a las ' + \
                strftime('%H:%M:%S', localtime())
        self.listw.addItem(message)
        self.listw.scrollToBottom()
        self.validKeyPressed = False

if __name__ == '__main__':
    app = QApplication(sys.argv)

    cummulative = MainWindow()
    cummulative.show()

    sys.exit(app.exec_())
