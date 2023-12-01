'''
This Software has been written for Machine Vision course and has no commercial use. Feel free to use and share.
Authors:
Amir M. Taghizadegan
Amir R. Radmanesh

*** Disclaimer of Warranty:
    This software is provided "as is" without any warranty, express or implied,
    including but not limited to the implied warranties of merchantability and
    fitness for a particular purpose. The authors make no representations or warranties
    regarding the use or performance of this software.

*** Limitation of Liability:
    In no event shall the authors be liable for any special, indirect, or consequential
    damages or any damages whatsoever resulting from loss of use, data, or profits, whether
    in an action of contract, negligence, or other tortious action, arising out of or in
    connection with the use or performance of this software.

*** Use at Your Own Risk:
    The use of this software is at your own risk. It is your responsibility to ensure that
    the software meets your requirements and is compatible with your system. The authors are
    not liable for any damages or issues arising from the use of this software.
'''

from PyQt6 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.signal import convolve2d
import numpy as np
import inspect
import sys
import os
import cv2

def Canny(image, threshold1=100, threshold2=200):
    return cv2.Canny(image, threshold1, threshold2)

def conv2d(img, kernel, mode = "same", boundry = "fill", fillValue = 0):
    return convolve2d(img, kernel, mode = mode, boundary=boundry, fillvalue=fillValue)

def filter2d(img, kernel, ddepth=-1):
    return cv2.filter2D(img, kernel=kernel, ddepth=ddepth)

class Main_Window(QtWidgets.QWidget):
    def __init__(self, pos = QtCore.QPoint(350, 150), size = (1200, 600)):
        super().__init__()
        # self.setGeometry(350, 150, 550, 350)
        self.window_size = size
        self.setGeometry(pos.x(), pos.y(), size[0], size[1])
        self.setWindowTitle("Machine Vision")
        self.setWindowIcon(QtGui.QIcon("images/logo.jpeg"))
        self.filterList = ["Canny", "conv2d", "filter2d"]
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
        windowmenu.addAction(QtGui.QIcon("images/Setting.png"), "Minimize", self.showMinimized)
        windowmenu.addAction(QtGui.QIcon("images/Setting.png"), "Maximize", self.showMaximized)
        windowmenu.addAction(QtGui.QIcon("images/Setting.png"), "Fullscreen", self.showFullScreen)

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
        self.apply_button.setFixedWidth(60)


        # drop down
        self.filter_dropdown = QtWidgets.QComboBox() 
        self.filter_dropdown.setFixedWidth(110)
        self.filter_dropdown.addItems(self.filterList)
        self.filter_dropdown.currentIndexChanged.connect(self.filter_change)

        # toolbar icons
        self.openFile_button.setIcon(QtGui.QIcon("images/plus_round.png"))
        self.openFile_button.setToolTip("Open image")
        self.saveFile_button.setIcon(QtGui.QIcon("images/save.png"))
        self.saveFile_button.setToolTip("Save image")
        self.saveAsFile_button.setIcon(QtGui.QIcon("images/save as.png"))
        self.saveAsFile_button.setToolTip("Save image as")
        self.apply_button.setText("Apply")
        self.apply_button.setIcon(QtGui.QIcon("images/submit.png"))
        self.apply_button.setToolTip("Submit")

        # connect
        self.openFile_button.clicked.connect(self.openFile_func)
        self.saveFile_button.clicked.connect(self.saveFile_func)
        self.saveAsFile_button.clicked.connect(self.saveAsFile_func)
        self.apply_button.clicked.connect(self.submit_func)
        self.filter_dropdown.currentIndexChanged.connect(self.filter_change)
        self.grayimage_checkbox.toggled.connect(self.image_toggle)


        ## figures
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.figure1.subplots_adjust(0, 0, 1, 1)
        self.figure2.subplots_adjust(0, 0, 1, 1)
        self.figure1.set_facecolor("none")
        self.figure2.set_facecolor("none")
        self.canvas1.setStyleSheet("background-color:transparent;")
        self.canvas2.setStyleSheet("background-color:transparent;")


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

        ## kernel
        self.kernel_checkbox = QtWidgets.QCheckBox("Kernel")
        self.kernel_size0 = QtWidgets.QTextEdit("3")
        self.kernel_label0 = QtWidgets.QLabel("x")
        self.kernel_size1 = QtWidgets.QTextEdit("3")
        self.kernel = QtWidgets.QTableWidget(int(self.kernel_size0.toPlainText()), int(self.kernel_size1.toPlainText()))
        self.create_kernel()

        self.kernel_button = QtWidgets.QPushButton("Create")
        self.kernel_button.setFixedWidth(125)

        self.kernel_checkbox.setMaximumSize(70, 28)
        self.kernel_flag = False
        self.kernel_size0.setFixedSize(QtCore.QSize(28, 28))
        self.kernel_size1.setFixedSize(QtCore.QSize(28, 28))
        self.kernel_label0.setFixedSize(QtCore.QSize(10, 28))

        # connect
        self.kernel_button.clicked.connect(self.create_kernel)
        self.kernel_checkbox.toggled.connect(self.change_kernelText)

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

        # kernel layout
        self.kernel_layout = QtWidgets.QVBoxLayout()
        self.kernel_barLayout = QtWidgets.QHBoxLayout()

        self.kernel_barLayout.addWidget(self.kernel_checkbox)
        self.kernel_barLayout.addWidget(self.kernel_size0)
        self.kernel_barLayout.addWidget(self.kernel_label0)
        self.kernel_barLayout.addWidget(self.kernel_size1)
        self.kernel_barLayout.addWidget(self.kernel_button)
        self.kernel_barLayout.setSpacing(4)

        self.kernel_layout.addLayout(self.kernel_barLayout)
        self.kernel_layout.addWidget(self.kernel)

        # toolbox layout
        self.toolbox = QtWidgets.QVBoxLayout()
        self.toolbox.addWidget(self.toolbox_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.toolbox.addWidget(self.textbox_label)
        self.toolbox.addWidget(self.textBox)
        self.toolbox.addLayout(self.kernel_layout)

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
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.path.curdir, "Image Files (*.png *.jpg *.jpeg *.bmp)")[0]
        try:
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
        except:
            self.statusBar.showMessage("please check your image and try again.", 10000)

    def saveFile_func(self):
        if not self.savePath:
            self.savePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.path.curdir, "Image Files (*.png *.jpg *.bmp)")
            if self.savePath:
                try:
                    cv2.imwrite(self.savePath, self.filteredImage)
                    self.statusBar.showMessage(f"File saved", 10000)
                except:
                    self.statusBar.update("Please submit a filter first", 10000)

    def saveAsFile_func(self):
        self.savePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.path.curdir, "Image Files (*.png *.jpg *.bmp)")
        if self.savePath:
            self.figure2.savefig(self.savePath)
            self.statusBar.showMessage(f"File saved as:\n{self.savePath}", 10000)

    def submit_func(self):
        inputs = self.textBox.toPlainText().strip().split("\n")
        if self.kernel_checkbox.isChecked():
            kernel = self.read_kernel()
        try:
            input = {list(inspect.signature(self.filter).parameters.items())[0][0]: self.img}
            try:
                inputs = dict([x.strip().split("=") for x in inputs])
                for key in inputs.keys():
                    try:
                        inputs[key] = eval(inputs[key])
                    except:
                        self.statusBar.showMessage("bad input. please make sure you are using valid libraries.")
                input.update(inputs)
                self.filteredImage = self.filter(**input)
                self.figure2.clear()
                ax = self.figure2.add_subplot()
                ndim = self.filteredImage.ndim
                if ndim  == 2:
                    ax.imshow(self.filteredImage, "gray")
                else:
                    ax.imshow(self.filteredImage)
                ax.axis(False)
                self.canvas2.draw()
                self.statusBar.showMessage(f"{self.currentFilterName} Filter applied", 10000)
            except ValueError:
                self.statusBar.showMessage("please check your inputs")
            except:
                self.statusBar.showMessage("something went wrong.")
        except AttributeError:
            self.statusBar.showMessage("please add an image first")
    
    def change_kernelText(self):
        text = self.textBox.toPlainText().strip()
        if self.kernel_checkbox.isChecked():
            if not self.kernel_flag:
                text = text + "\nkernel"
                self.textBox.setPlainText(text)
        else:
            if text.split("\n")[-1] == "kernel":
                text = text[:text.rfind('\n')]
                self.textBox.setPlainText(text)

    def create_kernel(self):
        try:
            x = eval(self.kernel_size0.toPlainText())
            y = eval(self.kernel_size1.toPlainText())
            self.kernelSize = (x, y)
            self.kernel.setRowCount(x)
            self.kernel.setColumnCount(y)
            for i in range(x):
                self.kernel.horizontalHeader().resizeSection(i, 10)
                for j in range(y):
                    self.kernel.verticalHeader().resizeSection(j, 10)
                    item = QtWidgets.QTableWidgetItem("0")
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.kernel.setItem(i, j, item)
        except:
            self.statusBar.showMessage("please check kernel size")
    
    def read_kernel(self):
        try:
            x, y = self.kernelSize
            kernel = np.empty(self.kernelSize)
            for i in range(x):
                for j in range(y):
                    kernel[i, j] = eval(self.kernel.item(i, j).text())
            return kernel
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return 0

    def filter_change(self):
        id = self.filter_dropdown.currentIndex()
        self.filter = eval(self.filterList[id])
        self.currentFilterName = self.filterList[id]
        text = [x+"\n" for x in inspect.signature(self.filter).__str__()[1:-1].split(", ")]
        self.kernel_checkbox.setChecked(False)
        if "kernel" in text:
            self.kernel_flag = True
            self.kernel_checkbox.setChecked(True)
            text[text.index("kernel")] += "=kernel"
        elif "kernel\n" in text:
            self.kernel_flag = True
            self.kernel_checkbox.setChecked(True)
            text[text.index("kernel\n")] = "kernel=kernel\n"
        else:
            self.kernel_flag = False
        self.textBox.setPlainText(''.join(text[1:]))
    
    def appSetting_func(self):
        pass

    def image_toggle(self):
        if self.figure1.get_axes():
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
            self.statusBar.showMessage(f"Input image channels changed!", 8000)
        else:
            self.statusBar.showMessage(f"Please open you image first.", 8000)
        

    def show_About_App(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setFixedSize(400,280)
        dlg.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        dlg.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        message = QtWidgets.QLabel("PLEASE HELP!", dlg)
        message.setWordWrap(True)
        message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        ok_button = QtWidgets.QPushButton("message received",dlg)
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