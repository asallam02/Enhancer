# This is the main python file to run the app
# rn just opens an empty window

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QStackedWidget,
    QPushButton
)

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        # create the window and set title
        super(MainWindow, self).__init__()
        self.setWindowTitle("Enhancer")

        # set the central widget 
        # NOTE: change this to a stacked widget later to have both pages
        # label = QLabel("Hello World")
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setCentralWidget(label)

        self.create_central_widget()
        self.create_buttons()
        
        button = QPushButton(self)
        button.setText("change central widget")
        button.move(64, 32)
        button.clicked.connect(self.button_clicked)

    def create_central_widget(self):
        firstWidget = QLabel("Widget 1")
        firstWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        secondWidget = QLabel("Widget 2")
        secondWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(firstWidget)
        self.stackedWidget.addWidget(secondWidget)

        self.setCentralWidget(self.stackedWidget)
        
    def button_clicked(self):
        self.stackedWidget.setCurrentIndex(1)

    def create_buttons(self):
        # create file open button
        open_btn = QAction("&Open", self)
        open_btn.setStatusTip("Open")
        open_btn.triggered.connect(self.onOpenBtnClick)

        # create file save button
        save_btn = QAction("&Save", self)
        save_btn.setStatusTip("Save")
        save_btn.triggered.connect(self.onSaveBtnClick)

        # create file new button
        new_btn = QAction("&New", self)
        new_btn.setStatusTip("New")
        new_btn.triggered.connect(self.onNewBtnClick)

        # create a menu bar
        menu = self.menuBar()

        # create a file menu and add open/save buttons
        file_menu = menu.addMenu("&File")
        file_menu.addAction(open_btn)
        file_menu.addAction(save_btn)
        file_menu.addAction(new_btn)

        menu.addSeparator()

        # create a home button and add to menu bar
        home_btn = QAction("&Home", self)
        home_btn.setStatusTip("Home")
        home_btn.triggered.connect(self.onHomeBtnClick)
        menu.addAction(home_btn)
    
    def onToolBarButtonClick(self, s):
        print("click", s)
    
    def saveSession(self):
        pass
    
    def openSession(self, filePath):
        pass

    def newSession(self, sessionName):
        pass

    def onHomeBtnClick(self):
        self.stackedWidget.setCurrentIndex(0)
        pass
    
    def onSaveBtnClick(self):
        self.saveSession()
    
    def onOpenBtnClick(self):
        # browse
        # get filepath
        filepath = ''
        # open session
        self.openSession(filepath)

    def onNewBtnClick(self):
        # ask for session name
        sessionName = ''
        # create session 
        self.newSession(sessionName)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = MainWindow()
    window.show()
    # start the event loop
    sys.exit(app.exec())