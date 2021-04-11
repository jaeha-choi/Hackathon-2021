import sys

import pyperclip
import qdarkstyle
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from pip._vendor.msgpack.fallback import xrange

import desktop_app.client as cl

RELAY_SERVER_IP = "143.198.234.58"
RELAY_SERVER_PORT = 1234


class MyWindow(QMainWindow):
    def __init__(self):

        super(MyWindow, self).__init__()
        self.setWindowTitle("Connect ME")

        # Establishes a Unique ID for the user
        self.yourUniqueID = uuid.uuid4()  # User's unique ID

        # Window setup
        self.xpos = 1920 // 3
        self.ypos = 1080 // 4
        self.dimension = 30
        self.aspectRatioWidth = 9
        self.aspectRatioHeight = 16

        self.windowWidth = self.dimension * self.aspectRatioWidth
        self.windowHeight = self.dimension * self.aspectRatioHeight

        # Show window
        self.setGeometry(self.xpos, self.ypos, self.windowWidth, self.windowHeight)
        # self.setWindowTitle("Connect ME")
        self.initUI()

        # SETUP CONNECTION

        self.client = cl.Client(RELAY_SERVER_IP, RELAY_SERVER_PORT)
        self.client.connect()
        self.client.send_uuid()

        # END OF CLIENT RECIEVER SETUP

    def initUI(self):
        layout = QVBoxLayout()

        # # Label Application Name
        # self.label = QtWidgets.QLabel(self)
        # self.label.setText("Connect ME")
        # self.label.move(self.windowWidth // 2.2, self.windowHeight // 32)

        # Set StyleSheet to Fusion by Default
        self.setStyleSheet('Fusion')

        # Delete File
        self.deleteFileButton = QPushButton(self)
        self.deleteFileButton.setText("Delete File(s)")
        self.deleteFileButton.clicked.connect(self.removeSel)

        # List of Files
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setGeometry(QtCore.QRect(120, 40, 256, 192))
        self.listWidget.setObjectName("listView")
        self.listWidget.move(50, 500)

        # Host Label Text
        self.yourUniqueIDLabel = QLabel(self)
        self.yourUniqueIDLabel.setText("Your Unique ID:")

        # Host Label Button: Copies to Clipboard
        self.hostLabelTextButton = QPushButton(self)
        self.hostLabelTextButton.setText(str(self.yourUniqueID))
        self.hostLabelTextButton.clicked.connect(self.hostLabel)

        # Host Field Text-Box
        self.hostFieldTextBox = QLineEdit(self)
        self.hostFieldTextBox.setPlaceholderText("Reciever's Unique ID")

        # Pick Files Button
        self.pickFilesButton = QPushButton(self)
        self.pickFilesButton.setText("Pick Files")
        self.pickFilesButton.move(self.windowWidth // 2, self.windowHeight // 4)
        self.pickFilesButton.clicked.connect(self.pickFiles)

        # Send Files Button
        # Will save the unique ID of the receiver when clicked as well
        self.sendFilesButton = QPushButton(self)
        self.sendFilesButton.setText("Send Files")
        self.sendFilesButton.move(self.windowWidth // 4, self.windowHeight // 4)
        self.sendFilesButton.clicked.connect(self.sendFiles)

        # Share Clipboard Contents
        self.shareClipboardButton = QPushButton(self)
        self.shareClipboardButton.setText("Share Copied Text")
        self.shareClipboardButton.clicked.connect(self.shareClipboard)

        # Dark Theme/Light Theme Button
        self.darkLightButton = QPushButton(self)
        self.darkLightButton.setText("Light")  # Light is set as default stylesheet mode
        self.darkLightButton.clicked.connect(self.darkLight)
        # Used to switch between dark and light mode
        self._darkLight_flag = True

        # Add Widgets to Layout
        layout.addWidget(self.deleteFileButton)
        layout.addWidget(self.listWidget)
        layout.addWidget(self.yourUniqueIDLabel)
        layout.addWidget(self.hostLabelTextButton)
        layout.addWidget(self.hostFieldTextBox)
        layout.addWidget(self.sendFilesButton)
        layout.addWidget(self.pickFilesButton)
        layout.addWidget(self.shareClipboardButton)
        layout.addWidget(self.darkLightButton)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

    def removeSel(self):
        listItems = self.listWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item))

    def hostLabel(self):
        pyperclip.copy(str(self.yourUniqueID))

    def pickFiles(self):
        # Mac OS
        fname = QFileDialog.getOpenFileNames(self, "Open File", "/Users/admin")
        self.listWidget.addItems(fname[0])

    def sendFiles(self):
        # Saves receiver's unique ID to a variable
        self.hostFieldValue = self.hostFieldTextBox.text()
        print(self.hostFieldValue)

        # SEND RECEIVER'S UNIQUE ID TO ESTABLISH SECURE CONNECTION
        # self.client.uuid = self.hostFieldValue
        # self.client.send_uuid()

        # Deals with saving and sending files
        items = []

        for index in xrange(self.listWidget.count()):
            items.append(self.listWidget.item(index))

        # Saves all the items as strings in the list in an array
        filePaths = [i.text() for i in items]
        fileNames = [j.split('/')[-1:][0] for j in filePaths]

        # SEND FILES TO RECIPIENT
        for filePath, fileName in zip(filePaths, fileNames):
            self.client.send_file(filePath, fileName)


    def shareClipboard(self):
        clipboardContents = pyperclip.paste()
        pyperclip.copy(clipboardContents)

    def darkLight(self):

        if (self._darkLight_flag == True):
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            self.darkLightButton.setText("Dark")
            self.deleteFileButton.setText("Murder File(s)")
            self._darkLight_flag = False

        elif (self._darkLight_flag == False):
            self.setStyleSheet('Fusion')
            self.darkLightButton.setText("Light")
            self.deleteFileButton.setText("Delete File(s)")
            self._darkLight_flag = True


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()
