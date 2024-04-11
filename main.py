# This is the main python file to run the app

'''
main flow
- on startup: make enformer object
- firstpage: make the query object
- variablepage: make the organizer object
- visualization: plot the graphs
'''

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
from frontPage import MainPage
from Models.Backend.Enformer import Enformer
from variablePage import VariablePage
from visualization import VizPage

class MainWindow(QMainWindow):
    def __init__(self):
        # create the window and set title
        super(MainWindow, self).__init__()
        self.setWindowTitle("Enhancer")

        model = Enformer()
        self.sequenceWidget = MainPage(model)
        self.variablePageWidget = VariablePage()
        self.vizPageWidget = VizPage()

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.sequenceWidget)
        self.stackedWidget.addWidget(self.variablePageWidget)
        self.stackedWidget.addWidget(self.vizPageWidget)

        self.setCentralWidget(self.stackedWidget)

        self.create_buttons()

        self.sequenceWidget.GoButton.clicked.connect(self.go_btn_clicked)
        self.variablePageWidget.next_button.clicked.connect(self.visualize)
        
    def go_btn_clicked(self):
        # save the data from this page
        self.queryToProcess = self.sequenceWidget.QueryToProcess
        # get results from enformer
        self.queryToProcess.calculate_enformer()

        # go to variable page
        self.variablePageWidget.originalSeq = self.queryToProcess.orig_result
        self.variablePageWidget.moddedSeq = self.queryToProcess.modded_result
        self.variablePageWidget.startpos = self.queryToProcess.start
        self.stackedWidget.setCurrentIndex(1)

    def visualize(self):
        # run the visualizations
        # create organizer object 
        self.variablePageWidget.go_to_next_page()

        # set objects in visualization page
        self.vizPageWidget.organizer = self.variablePageWidget.organizer
        self.vizPageWidget.query = self.queryToProcess

        # visualize
        self.vizPageWidget.plot_graphs()
        self.stackedWidget.setCurrentIndex(2)

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