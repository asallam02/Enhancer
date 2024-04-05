import sys
from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def SeqErrors(self, error_message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msgBox.setText(error_message)
        msgBox.setWindowTitle("Error")
        msgBox.addButton(QtWidgets.QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def SeqConditions(self, sequence, seqName):
        if not sequence:
            self.SeqErrors("Please enter a sequence.")
            return False

        if not seqName:
            self.SeqErrors("Please enter a sequence name.")
            return False

        if seqName in [seq[1] for seq in self.UserSeqs]:
            self.SeqErrors("Name already used. Please use a different name.")
            return False

        if sequence in [seq[0] for seq in self.UserSeqs]:
            existing_seq_name = [seq[1] for seq in self.UserSeqs if seq[0] == sequence][0]
            self.SeqErrors(f"Sequence already saved as '{existing_seq_name}'.")
            return False

        if not all(char.lower() in 'atcg' for char in sequence.lower()):
            self.SeqErrors("Sequence can only contain 'a', 't', 'c', or 'g'.")
            return False

        return True

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Horizontal layout for Start and Stop positions
        hbox = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(hbox)

        # Start Position LineEdit
        self.StartPos = QtWidgets.QLineEdit()
        self.StartPos.setPlaceholderText("Enter start nucleotide position ")
        hbox.addWidget(self.StartPos)

        # End Position LineEdit
        self.EndPos = QtWidgets.QLineEdit()
        self.EndPos.setPlaceholderText("Enter end nucleotide position ")
        hbox.addWidget(self.EndPos)

        # Nucleotide Position Button (Ok)
        self.NucPosButton = QtWidgets.QPushButton("Ok")
        hbox.addWidget(self.NucPosButton)
        self.NucPosButton.clicked.connect(self.validateAndEnableEditing)

        # Sequence Editor LineEdit
        self.SeqEditor = QtWidgets.QLineEdit()
        mainLayout.addWidget(self.SeqEditor)
        self.SeqEditor.setReadOnly(True)
        self.SeqEditor.setPlaceholderText("Edit Sequence Here")
        self.SeqEditor.setStyleSheet("font-size: 14px;")

        # Sequence Name LineEdit
        self.SeqName = QtWidgets.QLineEdit()
        self.SeqName.setPlaceholderText("Enter Sequence Name")
        mainLayout.addWidget(self.SeqName)

        # Add Sequence Button
        self.AddSeqButton = QtWidgets.QPushButton("Add Sequence")
        self.AddSeqButton.setMaximumWidth(100)
        mainLayout.addWidget(self.AddSeqButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Table Widget
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(3)
        mainLayout.addWidget(self.tableWidget)

        # Remove Button
        self.RemoveButton = QtWidgets.QPushButton("Remove Sequence")
        self.RemoveButton.setMaximumWidth(120)
        mainLayout.addWidget(self.RemoveButton)

        # Locus LineEdit and Ok Button
        locusLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(locusLayout)

        self.locusEdit = QtWidgets.QLineEdit()
        self.locusEdit.setPlaceholderText("Enter Locus")
        self.locusEdit.setMaximumWidth(200)
        locusLayout.addWidget(self.locusEdit)

        self.OkButton = QtWidgets.QPushButton("Ok")
        self.OkButton.setMaximumWidth(100)
        locusLayout.addWidget(self.OkButton)

        # Go! Button
        self.GoButton = QtWidgets.QPushButton("Go!")
        self.GoButton.setMaximumWidth(100)
        mainLayout.addWidget(self.GoButton, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.UserSeqs = []

        self.AddSeqButton.clicked.connect(self.addSequence)
        self.RemoveButton.clicked.connect(self.removeSequence)
        self.OkButton.clicked.connect(self.saveLocus)
        self.GoButton.clicked.connect(self.goNext)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.AddSeqButton.setText(_translate("MainWindow", "Add Sequence"))
        self.RemoveButton.setText(_translate("MainWindow", "Remove Sequence"))
        self.tableWidget.setHorizontalHeaderLabels(["", "Sequence Name", "Sequence"])

    def validateAndEnableEditing(self):
        startSeq = self.StartPos.text()
        endSeq = self.EndPos.text()

        errors = []
        if not startSeq.isdigit() or not endSeq.isdigit():
            errors.append("Start and end positions must be positive whole numbers.")
        elif int(startSeq) <= 0 or int(endSeq) <= 0:
            errors.append("Start and end positions must be greater than 0.")
        elif int(startSeq) >= int(endSeq):
            errors.append("Start position must be less than end position.")

        if errors:
            error_message = "\n".join(errors)
            self.showErrorMessageBox(error_message)
        else:
            subSeq = "acctagactcatcaagctgtcggca"
            self.SeqEditor.setText(subSeq)
            self.SeqEditor.setReadOnly(False)

    def showErrorMessageBox(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle("Error")
        msgBox.addButton(QtWidgets.QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def addSequence(self):
        sequence = self.SeqEditor.text()
        seqName = self.SeqName.text()

        if not self.SeqConditions(sequence, seqName):
            return

        self.UserSeqs.append((sequence, seqName))
        self.updateTable()

    def updateTable(self):
        self.tableWidget.setRowCount(len(self.UserSeqs))
        for row, (sequence, seqName) in enumerate(self.UserSeqs):
            checkbox_item = QtWidgets.QTableWidgetItem()
            checkbox_item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            checkbox_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.tableWidget.setItem(row, 0, checkbox_item)  
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(seqName))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(sequence))

        self.tableWidget.horizontalHeader().setStretchLastSection(True)

    def removeSequence(self):
        selected_rows = [index for index in range(self.tableWidget.rowCount()) if self.tableWidget.item(index, 0).checkState() == QtCore.Qt.CheckState.Checked]
        for row in sorted(selected_rows, reverse=True):
            del self.UserSeqs[row]
        self.updateTable()

    def saveLocus(self):
        locus_value = self.locusEdit.text()
        if not self.locusConditions(locus_value):
            self.showErrorMessageBox("Please enter the locus in genome coordinate format.")
            return
        print("Locus saved:", locus_value)

    def locusConditions(self, text):
        parts = text.split(':')
        if len(parts) != 2:
            return False
        if not parts[0].isdigit() or not parts[1].isdigit():
            return False
        return True

    def goNext(self):
        print("Go! button clicked")
        print(self.UserSeqs)

    def startEndConditions(self, text):
        if not all(char.lower() in 'atcg' for char in text.lower()):
            self.SeqErrors("Sequence can only contain ATCG.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
