'''This is the main page that runs the GUI.
To run this page first ensure that you have
the needed packages downloaded and then run 
py main.py from the terminal. 

This page will do several things, it will 
first set up the app by creating the ML model 
object (Enformer). It will show a page for 
sequence entry by the user, followed by a page
for variable entry, and lastly a page for 
visualization.
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
from visualizationPage import VizPage

class MainWindow(QMainWindow):
    def __init__(self):
        # create the window and set title
        super(MainWindow, self).__init__()
        self.setWindowTitle("Enhancer")

        # create model object
        model = Enformer()

        # create the three pages 
        self.sequencePageWidget = MainPage(model)
        self.variablePageWidget = VariablePage()
        self.vizPageWidget = VizPage()

        # create a stacked widget and add the pages
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.sequencePageWidget)
        self.stackedWidget.addWidget(self.variablePageWidget)
        self.stackedWidget.addWidget(self.vizPageWidget)

        # set the central widget for the GUI
        self.setCentralWidget(self.stackedWidget)

        self.create_buttons()

        # connect buttons to their corresponding functions
        self.sequencePageWidget.GoButton.clicked.connect(self.go_btn_clicked)
        self.variablePageWidget.next_button.clicked.connect(self.visualize)
        
    def go_btn_clicked(self):
        '''Function for when go button is clicked on the sequence entry page
        This is where enformer gets called and then the UI switches to the
        get variable page.
        '''
        # save the data from this page
        self.queryToProcess = self.sequencePageWidget.QueryToProcess
        # get results from enformer
        self.queryToProcess.calculate_enformer()

        # save enformer results
        self.variablePageWidget.originalSeq = self.queryToProcess.orig_result
        self.variablePageWidget.moddedSeq = self.queryToProcess.modded_result
        self.variablePageWidget.startpos = self.queryToProcess.start

        # go to variable page
        self.stackedWidget.setCurrentIndex(1)

    def visualize(self):
        '''Function for when next button is clicked on the variable entry page
        This is where the graphs are created and shown on the visualization 
        page.
        '''
        # create organizer object 
        self.variablePageWidget.go_to_next_page()

        # set objects in visualization page
        self.vizPageWidget.organizer = self.variablePageWidget.organizer
        self.vizPageWidget.query = self.queryToProcess

        # plot graphs
        self.vizPageWidget.plot_graphs()

        # switch to visualizaion page
        self.stackedWidget.setCurrentIndex(2)

    def create_buttons(self):
        '''Helper function to create the buttons on the menu bar.
        Creates the file menu with open, save, and new buttons. 
        Creates a home button that goes back to the sequence entry
        page when clicked. 
        '''
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
    
    # the function below are not yet implemented, this is 
    # what will implement the memory functionality of the 
    # application
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