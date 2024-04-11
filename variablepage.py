import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QScrollArea, QMessageBox
from Models.Graphing.Organizer import Organizer

class VariablePage(QWidget):
    originalSeq = None
    moddedSeq = None

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

        self.box_layouts = []

        # Insert Section
        self.input_layout = QHBoxLayout()
        self.input_labels = ['Start:', 'Stop:', 'magnitude:', 'neighbours:', 'cluster size:']
        self.input_fields = [QLineEdit() for _ in range(len(self.input_labels))]

        for label, field in zip(self.input_labels, self.input_fields):
            self.input_layout.addWidget(QLabel(label))
            self.input_layout.addWidget(field)

        self.add_box_button = QPushButton('Add Box')
        self.add_box_button.clicked.connect(self.add_box)

        self.insert_section = QWidget()
        insert_section_layout = QVBoxLayout()
        insert_section_layout.addLayout(self.input_layout)
        insert_section_layout.addWidget(self.add_box_button)
        self.insert_section.setLayout(insert_section_layout)

        self.main_layout.addWidget(self.insert_section)

        # Scroll Area for Boxes
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.main_layout.addWidget(self.scroll_area)

        # Next Button
        self.next_button = QPushButton('Next')
        # self.next_button.clicked.connect(self.go_to_next_page)
        self.main_layout.addWidget(self.next_button)

        self.setLayout(self.main_layout)

    def add_box(self):
        # Get values from input fields
        values = [field.text() for field in self.input_fields]

        # Validation checks
        try:
            value_1 = int(values[0])
            value_2 = int(values[1])
            value_3 = float(values[2])
            value_4 = int(values[3])
            value_5 = int(values[4])

            if value_1 <= 0 or value_2 <= 0 or value_2 <= value_1:
                QMessageBox.critical(self, 'Error', 'Variable 1 must be a positive integer, Variable 2 must be a positive integer greater than Variable 1.')
                return
            if value_3 <= 0:
                QMessageBox.critical(self, 'Error', 'Variable 3 must be a positive float.')
                return
            if value_4 <= 0 or value_5 <= 0:
                QMessageBox.critical(self, 'Error', 'Variable 4 and Variable 5 must be positive non-zero integers.')
                return

        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid input. Please enter valid numbers.')
            return

        # If all checks pass, proceed to add the box
        box_layout = QHBoxLayout()
        box_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to ensure fixed size

        for value in values:
            label = QLabel(value)
            box_layout.addWidget(label)

        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda checked, layout=box_layout: self.delete_box(layout))
        box_layout.addWidget(delete_button)

        self.box_layouts.append(box_layout)
        self.scroll_area_layout.addLayout(box_layout)

    def delete_box(self, layout):
        for i in reversed(range(self.scroll_area_layout.count())):
            item = self.scroll_area_layout.itemAt(i)
            if isinstance(item, QHBoxLayout) and item == layout:
                for j in reversed(range(layout.count())):
                    widget = layout.itemAt(j).widget()
                    if widget is not None:
                        widget.deleteLater()
                self.scroll_area_layout.removeItem(item)
                self.box_layouts.remove(layout)
                break

    def go_to_next_page(self):
        # make sure original and modded are a initialized
        # if (self.originalSeq == None or self.moddedSeq == None):
        #     raise ValueError("variable page: need to initalize sequences first")
        
        # create organizer object
        self.organizer = Organizer(self.originalSeq, self.moddedSeq, self.startpos)
        print("created organizer object")

        # get values from user input
        j = 0
        for layout in self.box_layouts:
            values = []
            for i in range(layout.count() - 1):  # Exclude the delete button
                widget = layout.itemAt(i).widget()
                if isinstance(widget, QLabel):
                    values.append(float(widget.text()))
            print(values)
            self.organizer.add_box(j, int(values[0]), int(values[1]), values[2], int(values[3]), int(values[4]), genRandomColor())
            j += 1


def genRandomColor():
    hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
    return hexadecimal      


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()

    box_widget = VariablePage()
    layout.addWidget(box_widget)

    window.setLayout(layout)
    window.setWindowTitle('Box Record')
    window.setGeometry(100, 100, 400, 300)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
