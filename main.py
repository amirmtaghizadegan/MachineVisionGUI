from PyQt6 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from imageio import imread, imsave, imopen
from matplotlib.figure import Figure
import inspect
import sys
import os
import cv2

def Canny(image, threshold1=100, threshold2=200):
        return cv2.Canny(image, threshold1, threshold2)

class Main_Window(QtWidgets.QWidget):
    def __init__(self, pos = QtCore.QPoint(350, 150), size = (1200, 600)):
        super().__init__()
        # self.setGeometry(350, 150, 550, 350)
        self.window_size = size
        self.setGeometry(pos.x(), pos.y(), size[0], size[1])
        self.setWindowTitle("Machine Vision")
        self.setWindowIcon(QtGui.QIcon("images/logo.jpeg"))
        self.filterList = ["Canny"]
        self.filter = Canny
        self.UI()
        self.filter_change()

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
        editmenu.addAction(QtGui.QIcon("images/Setting.png"), "Setting", self.appSetting_func)

        # Window menu
        windowmenu = self.menubar.addMenu("&Window")
        windowmenu.addAction(QtGui.QIcon("images/Setting.png"), "Minimize")
        windowmenu.addAction(QtGui.QIcon("images/Setting.png"), "Maximize")
        windowmenu.addAction(QtGui.QIcon("images/Setting.png"), "Fullscreen")

        # Help menu
        helpmenu = self.menubar.addMenu("&Help")
        helpmenu.addAction(QtGui.QIcon("images/info_round.png"), "About", self.show_About_App)


        ## toolbar
        # buttons
        self.openFile_button = QtWidgets.QPushButton()
        self.grayimage_checkbox = QtWidgets.QCheckBox("Grayscale image")
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
        self.filter_dropdown.currentIndexChanged.connect(self.filter_change)

        ## figures
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)

        ## toolbox
        # titles
        self.toolbox_label = QtWidgets.QLabel("Filter Settings")
        self.toolbox_label.setStyleSheet("QLabel{font-size: 10pt; font-weight: bold;}")
        self.textbox_label = QtWidgets.QLabel("Hyper Parameters:")

        # hyper parameters
        self.textBox = QtWidgets.QPlainTextEdit()
        self.textBox.setFixedSize(int(1/4*self.window_size[0]), int(1/4*self.window_size[1]))
        text = [x+"\n" for x in inspect.signature(self.filter).__str__()[1:-1].split(", ")]
        self.textBox.setPlainText(''.join(text[1:]))

        ## status bar
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.showMessage('Ready')


    def layouts(self):
        # toolbar layout
        self.toolbar = QtWidgets.QHBoxLayout()
        self.toolbar.addWidget(self.openFile_button)
        self.toolbar.addWidget(self.grayimage_checkbox)
        self.toolbar.addWidget(self.saveFile_button)
        self.toolbar.addWidget(self.saveAsFile_button)
        self.toolbar.addWidget(self.filter_dropdown)
        self.toolbar.addWidget(self.apply_button)
        self.toolbar.addStretch()

        # toolbox layout
        self.toolbox = QtWidgets.QVBoxLayout()
        self.toolbox.addWidget(self.toolbox_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
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
            ax = self.figure1.add_subplot()
            if self.grayimage_checkbox.isChecked():
                self.img = cv2.imread(self.path, 0)
                ax.imshow(self.img, cmap="gray")
            else:
                self.img = cv2.imread(self.path)
                self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                ax.imshow(self.img)
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
        inputs = self.textBox.toPlainText()
        try:
            input = {list(inspect.signature(self.filter).parameters.items())[0][0]: self.img}
            try:
                inputs = inputs.split("\n")
                inputs = dict([x.strip().split("=") for x in inputs[:-1]])
                for key in inputs.keys():
                    try:
                        inputs[key] = eval(inputs[key])
                    except:
                        self.statusBar.showMessage("bad input. please make sure you are using valid libraries.")
                input.update(inputs)
                self.filteredImage = self.filter(**input)
                # self.filteredImage = self.filter(self.img[:, :, 1], 100, 200)
                self.figure2.clear()
                ax = self.figure2.add_subplot()
                if self.grayimage_checkbox.isChecked():
                    ax.imshow(self.filteredImage, "gray")
                else:
                    ax.imshow(self.filteredImage)
                ax.axis(False)
                self.canvas2.draw()
                self.statusBar.showMessage(f"{self.currentFilterName} Filter applied", 10000)
            except ValueError:
                print(input)
                print("--------------------")
                print(inputs)
                self.statusBar.showMessage("please check your inputs")
            except:
                self.statusBar.showMessage("Something went wrong. Please check your input values")
        except AttributeError:
            self.statusBar.showMessage("please add an image first")
        
        

    def filter_change(self):
        id = self.filter_dropdown.currentIndex()
        choice = self.filterList[id]
        self.currentFilterName = choice
        if (choice=="Canny"):
            self.filter = Canny

    def appSetting_func(self):
        pass

    def show_About_App(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setFixedSize(220,280)
        dlg.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        dlg.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        message = QtWidgets.QLabel(":) This application developed by a great Team that prisoned in iran so if you see this message\n\nPLEASE HELP US :_(", dlg)
        message.setWordWrap(True)
        message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        ok_button = QtWidgets.QPushButton("COOL!",dlg)
        about_layout = QtWidgets.QVBoxLayout()
        about_layout.addWidget(message)
        about_layout.addWidget(ok_button)
        dlg.setLayout(about_layout)
        ok_button.clicked.connect(dlg.close)
        dlg.setWindowTitle("Hallo!")
        dlg.exec()

    

    def exitApp_func(self):
        exit()





if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("./images/logo.jpeg"))
    window = Main_Window()
    window.show()
    sys.exit(app.exec())