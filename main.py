# This is the main python file to run the app
# rn just opens an empty window

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget
)

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('GeneCAD')

        # make sure to add widgets here for them to show

        # show the window
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = MainWindow()

    # start the event loop
    sys.exit(app.exec())