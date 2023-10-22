import typing
from PyQt6 import QtWidgets, QtCore, QtGui
import sys

from PyQt6.QtWidgets import QLayout

class Main_Window(QtWidgets.QWidget):
    def __init__(self, pos = QtCore.QPoint(350, 150), size = (600, 350)):
        super().__init__()
        self.setGeometry(350, 150, 550, 350)
        self.setGeometry(pos.x(), pos.y(), size[0], size[1])
        self.setWindowTitle("Main Menu")
        self.setWindowIcon(QtGui.QIcon("images/logo.jpeg"))
        self.UI()
        self.show()


    def mainDesign(self):
        # buttons
        self.openFile_button = QtWidgets.QPushButton("open file")
        self.saveFile_button = QtWidgets.QPushButton("save file")
        self.saveAsFile_button = QtWidgets.QPushButton("save file")
        self.apply_button = QtWidgets.QPushButton("apply")

        # Set icons for the buttons
        self.openFile_button.setIcon(QtGui.QIcon("button1_icon.png"))
        self.saveFile_button.setIcon(QtGui.QIcon("button2_icon.png"))
        self.saveAsFile_button.setIcon(QtGui.QIcon("button3_icon.png"))
        self.apply_button.setIcon(QtGui.QIcon("button4_icon.png"))

        # 

    def layouts(self):
        # toolbox layout
        self.toolbox = QtWidgets.QHBoxLayout()
        self.toolbox.addItem(self.openFile_button)
        self.toolbox.addItem(self.saveFile_button)
        self.toolbox.addItem(self.saveAsFile_button)
        self.toolbox.addItem(self.apply_button)

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
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
    print("amir reza khar ast")