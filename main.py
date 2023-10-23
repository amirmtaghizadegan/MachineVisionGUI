import typing
from PyQt6 import QtWidgets, QtCore, QtGui
import sys

from PyQt6.QtWidgets import QLayout

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

        # 

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

        # central layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.toolbox)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def UI(self):
        self.mainDesign()
        self.layouts()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("./images/logo.jpeg"))
    window = Main_Window()
    window.show()
    sys.exit(app.exec())