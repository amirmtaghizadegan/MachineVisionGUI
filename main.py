from PyQt6 import QtWidgets, QtCore, QtGui
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        ## menu bar
        self.menubar = QtWidgets.QMenuBar(self)
        # File menu
        filemenu = self.menubar.addMenu("&File")
        # filemenu.addAction(self.openFile_func) ADD self.openfile_func
        # filemenu.addAction(self.saveAction) ADD self.saveFile_func
        # filemenu.addAction(self.saveeasAction) ADD self.saveAsFile_func
        # filemenu.addAction(self.exitAction) ADD self.exitAction_func

        # Edit menu
        editMenu = self.menubar.addMenu("&Edit")
        # Add edit actions later ...

        # Help menu
        helpMenu = self.menubar.addMenu("&Help")
        # Add help menu later ...


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

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("./images/logo.jpeg"))
    window = Main_Window()
    window.show()
    sys.exit(app.exec())