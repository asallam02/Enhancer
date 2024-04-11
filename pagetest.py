import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QScrollArea


class BoxWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.box_layouts = []

        self.add_box_button = QPushButton('Add Box')
        self.add_box_button.clicked.connect(self.add_box)
        self.layout.addWidget(self.add_box_button)

        self.setLayout(self.layout)

    def add_box(self):
        box_layout = QVBoxLayout()

        variables_layout = QHBoxLayout()

        box_groupbox = QGroupBox()
        self.box_layouts.append(box_layout)

        for var in ['start', 'stop', 'magnitude', 'neighbours', 'cluster size']:
            var_label = QLabel(f'{var}:')
            var_input = QLineEdit()
            variables_layout.addWidget(var_label)
            variables_layout.addWidget(var_input)

        box_groupbox.setLayout(variables_layout)

        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda checked, box_layout=box_layout: self.delete_box(box_layout))
        box_layout.addWidget(box_groupbox)
        box_layout.addWidget(delete_button)

        self.layout.addLayout(box_layout)

    def delete_box(self, box_layout):
        for i in reversed(range(box_layout.count())):
            widget = box_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.layout.removeItem(box_layout)
        self.box_layouts.remove(box_layout)


class NextPageWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel('This is the next page.')
        layout.addWidget(label)

        self.setLayout(layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.current_widget = BoxWidget()
        self.next_page_widget = NextPageWidget()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        button = QPushButton('Next Page')
        button.clicked.connect(self.show_next_page)
        self.layout.addWidget(button)

        self.layout.addWidget(self.current_widget)

        self.setLayout(self.layout)
        self.setWindowTitle('Main Window')

    def show_next_page(self):
        self.layout.removeWidget(self.current_widget)
        self.current_widget.hide()
        self.layout.addWidget(self.next_page_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
