# This is the main python file to run the app
# rn just opens an empty window

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # show the window
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = MainWindow()

    # start the event loop
    sys.exit(app.exec())