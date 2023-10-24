from PyQt6 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from imageio import imread, imsave, imopen
from matplotlib.figure import Figure
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
import os
import cv2

class Main_Window(QtWidgets.QWidget):
    def __init__(self, pos = QtCore.QPoint(350, 150), size = (1200, 600)):
        super().__init__()
        # self.setGeometry(350, 150, 550, 350)
        self.window_size = size
        self.setGeometry(pos.x(), pos.y(), size[0], size[1])
        self.setWindowTitle("Machine Vision")
        self.setWindowIcon(QtGui.QIcon("images/logo.jpeg"))
        self.filterList = ["Canny"]
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


        ## toolbar
        # buttons
        self.openFile_button = QtWidgets.QPushButton()
        self.saveFile_button = QtWidgets.QPushButton()
        self.saveAsFile_button = QtWidgets.QPushButton()
        self.apply_button = QtWidgets.QPushButton()

        # drop down
        self.filter_dropdown = QtWidgets.QComboBox() 
        self.filter_dropdown.addItems(self.filterList)
        # self.filter_dropdown.changeEvent()

        # toolbar icons
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

        ## figures
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)

        ## toolbox
        # titles
        self.toolbox_label = QtWidgets.QLabel("Filter Setting")
        self.toolbox_label.setStyleSheet("QLabel{font-size: 10pt; font-weight: bold;}")
        self.textbox_label = QtWidgets.QLabel("Hyper Parameters:")

        # hyper parameters
        self.textBox = QtWidgets.QPlainTextEdit()
        self.textBox.setFixedSize(int(1/4*self.window_size[0]), int(1/4*self.window_size[1]))

        ## status bar
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.showMessage('Ready')


    def layouts(self):
        # toolbar layout
        self.toolbar = QtWidgets.QHBoxLayout()
        self.toolbar.addWidget(self.openFile_button)
        self.toolbar.addWidget(self.saveFile_button)
        self.toolbar.addWidget(self.saveAsFile_button)
        self.toolbar.addWidget(self.filter_dropdown)
        self.toolbar.addWidget(self.apply_button)
        self.toolbar.addStretch()

        # toolbox layout
        self.toolbox = QtWidgets.QVBoxLayout()
        self.toolbox.addWidget(self.toolbox_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.toolbox.addWidget(self.textbox_label)
        self.toolbox.addWidget(self.textBox)
        self.toolbox.addStretch()

        # plot layout
        self.plot_layout = QtWidgets.QHBoxLayout()
        self.plot_layout.addWidget(self.canvas1)
        self.plot_layout.addWidget(self.canvas2)
        self.plot_layout.addLayout(self.toolbox)
        
        # central layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.menubar)
        self.main_layout.addLayout(self.toolbar)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.plot_layout)
        self.main_layout.addWidget(self.statusBar)
        self.setLayout(self.main_layout)
        
    def UI(self):
        self.mainDesign()
        self.layouts()

    def openFile_func(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.path.curdir, "Image Files (*.png *.jpg *.bmp)")[0]
        if self.path:
            self.figure1.clear()
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
        id = self.filter_dropdown.currentIndex()
        choice = self.filterList[id]
        if (choice=="Canny"):
            self.filteredImage = cv2.Canny(self.img,100,200)
        self.figure2.clear()
        ax = self.figure2.add_subplot()
        if len(self.filteredImage.shape) > 2:
            ax.imshow(self.filteredImage)
        else:
            ax.imshow(self.filteredImage, "gray")
        ax.axis(False)
        self.canvas2.draw()
        self.statusBar.showMessage(f"{choice} Filter applied", 10000)

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