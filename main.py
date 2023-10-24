from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
from imageio import imread, imsave, imopen

class Main_Window(QtWidgets.QWidget):
    def __init__(self, pos = QtCore.QPoint(350, 150), size = (800, 600)):
        super().__init__()
        # self.setGeometry(350, 150, 550, 350)
        self.setGeometry(pos.x(), pos.y(), size[0], size[1])
        self.setWindowTitle("Machine Vision")
        self.setWindowIcon(QtGui.QIcon("images/logo.jpeg"))
        self.UI()

        self.savePath = ""
        
        self.show()


    def mainDesign(self):
        ## menu bar
        self.menubar = QtWidgets.QMenuBar(self)
        # File menu
        filemenu = self.menubar.addMenu("&File")
        filemenu.addAction(QtGui.QIcon("images/open_file.png"), "Open File", self.openFile_func)
        filemenu.addAction(QtGui.QIcon("images/save.png"), "Save", self.saveFile_func)
        filemenu.addAction(QtGui.QIcon("images/save as.png"), "Save as", self.saveAsFile_func)
        filemenu.addAction(QtGui.QIcon("images/exit.png"), "Exit",self.exitApp_func)

        # Edit menu
        editmenu = self.menubar.addMenu("&Edit")
        editmenu.addAction("Setting", self.appSetting_func)

        # Help menu
        helpmenu = self.menubar.addMenu("&Help")
        helpmenu.addAction(QtGui.QIcon("images/info_round.png"), "About")


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
        self.openFile_button.setIcon(QtGui.QIcon("images/plus_round.png"))
        self.openFile_button.setToolTip("Open image")
        self.saveFile_button.setIcon(QtGui.QIcon("images/save.png"))
        self.saveFile_button.setToolTip("Save image")
        self.saveAsFile_button.setIcon(QtGui.QIcon("images/save as.png"))
        self.saveAsFile_button.setToolTip("Save image as")
        self.apply_button.setIcon(QtGui.QIcon("images/submit.png"))
        self.apply_button.setToolTip("Submit")

         # connect
        self.openFile_button.clicked.connect(self.openFile_func)
        self.saveFile_button.clicked.connect(self.saveFile_func)
        self.saveAsFile_button.clicked.connect(self.saveAsFile_func)
        self.apply_button.clicked.connect(self.submit_func)

        # figures
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)

        # status bar
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.showMessage('Ready')


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
        self.main_layout.addWidget(self.menubar)
        self.main_layout.addLayout(self.toolbox)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.plot_layout)
        self.main_layout.addWidget(self.statusBar)
        self.setLayout(self.main_layout)
        
    def UI(self):
        self.mainDesign()
        self.layouts()

    def openFile_func(self):
        self.figure1.clear()
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.path.curdir, "Image Files (*.png *.jpg *.bmp)")[0]
        if self.path:
            self.img = imread(self.path)
            ax = self.figure1.add_subplot()
            if self.img.shape[2] > 1:
                ax.imshow(self.img)
            else:
                ax.imshow(self.img, "gray")
            ax.axis(False)
            self.canvas1.draw()
            self.statusBar.showMessage(f"File: {self.path}", 10000)

    def saveFile_func(self):
        if self.savePath:
            self.figure2.savefig(self.savePath)
            self.statusBar.showMessage(f"File saved", 10000)
        else:
            self.savePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.path.curdir, "Image Files (*.png *.jpg *.bmp)")
            if self.savePath:
                self.figure2.savefig(self.savePath)
                self.statusBar.showMessage(f"File saved", 10000)

    def saveAsFile_func(self):
        self.savePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.path.curdir, "Image Files (*.png *.jpg *.bmp)")
        if self.savePath:
            self.figure2.savefig(self.savePath)
            self.statusBar.showMessage(f"File saved as:\n{self.savePath}", 10000)

    def submit_func(self):
        pass

    def appSetting_func(self):
        pass

    def exitApp_func(self):
        exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("./images/logo.jpeg"))
    window = Main_Window()
    window.show()
    sys.exit(app.exec())