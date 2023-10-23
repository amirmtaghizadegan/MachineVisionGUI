from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
from imageio import imread, imsave, imopen

class Main_Window(QtWidgets.QWidget):
    def __init__(self, pos = QtCore.QPoint(350, 150), size = (600, 350)):
        super().__init__()
        self.setGeometry(350, 150, 550, 350)
        self.setGeometry(pos.x(), pos.y(), size[0], size[1])
        self.setWindowTitle("Machine Vision")
        self.setWindowIcon(QtGui.QIcon("images/logo.jpeg"))
        self.UI()
        self.show()


    def mainDesign(self):
        ## toolbox
        # buttons
        self.openFile_button = QtWidgets.QPushButton()
        self.saveFile_button = QtWidgets.QPushButton()
        self.saveAsFile_button = QtWidgets.QPushButton()
        self.apply_button = QtWidgets.QPushButton()
        
        # drop down
        self.filter_list = QtWidgets.QComboBox() 
        self.filter_list.addItem("hello")

        # toolbox icons
        self.openFile_button.setIcon(QtGui.QIcon("images/open_file.png"))
        self.saveFile_button.setIcon(QtGui.QIcon("images/save.png"))
        self.saveAsFile_button.setIcon(QtGui.QIcon("images/save as.png"))
        self.apply_button.setIcon(QtGui.QIcon("images/submit.png"))

        # connect
        self.openFile_button.clicked.connect(self.openFile_func)
        self.saveFile_button.clicked.connect(self.saveFile_func)
        self.saveAsFile_button.clicked.connect(self.saveAsFile_func)
        self.apply_button.clicked.connect(self.submit_func)

        ## figures
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
         
    def layouts(self):
        # toolbox layout
        self.toolbox = QtWidgets.QHBoxLayout()
        self.toolbox.addWidget(self.openFile_button)
        self.toolbox.addWidget(self.saveFile_button)
        self.toolbox.addWidget(self.saveAsFile_button)
        self.toolbox.addWidget(self.filter_list)
        self.toolbox.addWidget(self.apply_button)
        self.toolbox.addStretch()

        # hyper parameters layout

        # plot layout
        self.plot_layout = QtWidgets.QHBoxLayout()
        self.plot_layout.addWidget(self.canvas1)
        self.plot_layout.addWidget(self.canvas2)
        
        # central layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.toolbox)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.plot_layout)
        self.setLayout(self.main_layout)

    def UI(self):
        self.mainDesign()
        self.layouts()

    def openFile_func(self):
        self.figure1.clear()
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.path.curdir, "Image Files (*.png *.jpg *.bmp)")[0]
        self.img = imread(self.path)
        ax = self.figure1.add_subplot()
        if self.img.shape[2] > 1:
            ax.imshow(self.img)
        else:
            ax.imshow(self.img, "gray")
        ax.axis(False)
        self.canvas1.draw()

    def saveFile_func(self):
        pass

    def saveAsFile_func(self):
        pass

    def submit_func(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("./images/logo.jpeg"))
    window = Main_Window()
    window.show()
    sys.exit(app.exec())