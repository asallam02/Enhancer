import sys
from PyQt6 import QtCore, QtWidgets

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

    def obsStartStopConditions(self, obsStart, obsStop):
        try:
            start_int = int(obsStart)
            stop_int = int(obsStop)
            if start_int <= 0 or stop_int <= 0:
                self.SeqErrors("Start and end positions must be greater than 0.")
                return False
            elif start_int >= stop_int:
                self.SeqErrors("Start position must be less than end position.")
                return False
        except ValueError:
            self.SeqErrors("Start and end positions must be positive integers.")
            return False
        
        return True

    def chromoConditions(self, chromosome):
        try:
            if chromosome.lower() not in ['x', 'y'] and not (1 <= int(chromosome) <= 22):
                self.SeqErrors("Chromosome must be an integer between 1 and 22, or 'x' or 'y'.")
                return False
        except ValueError:
            self.SeqErrors("Chromosome must be an integer between 1 and 22, or 'x' or 'y'.")
            return False
        
        return True


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Location for Chromosome Header
        chromoHeader = QtWidgets.QLabel("Location in Chromosome:")
        mainLayout.addWidget(chromoHeader)

        # Horizontal layout for Chromosome Entry
        chromoLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(chromoLayout)

        # Chromosome LineEdit
        self.ChromosomeEdit = QtWidgets.QLineEdit()
        self.ChromosomeEdit.setPlaceholderText("Enter Chromosome")
        self.ChromosomeEdit.setMaximumWidth(200)
        chromoLayout.addWidget(self.ChromosomeEdit)

        # Start Observable LineEdit
        self.obsStartPos = QtWidgets.QLineEdit()
        self.obsStartPos.setPlaceholderText("Enter start position")
        self.obsStartPos.setMaximumWidth(200)
        chromoLayout.addWidget(self.obsStartPos)

        # End Observable LineEdit
        self.obsEndPos = QtWidgets.QLineEdit()
        self.obsEndPos.setPlaceholderText("Enter stop position")
        self.obsEndPos.setMaximumWidth(200)
        chromoLayout.addWidget(self.obsEndPos)

        # Add Observable Range Button
        self.AddRangeButton = QtWidgets.QPushButton("Ok")
        self.AddRangeButton.setMaximumWidth(100)
        chromoLayout.addWidget(self.AddRangeButton)
        self.AddRangeButton.clicked.connect(self.saveObservableRange)

        # Labels for displaying input values
        self.chromoLabel = QtWidgets.QLabel()
        mainLayout.addWidget(self.chromoLabel)
        self.obsStartLabel = QtWidgets.QLabel()
        mainLayout.addWidget(self.obsStartLabel)
        self.obsStopLabel = QtWidgets.QLabel()
        mainLayout.addWidget(self.obsStopLabel)

        # Subsequence Editing Header
        subseqHeader = QtWidgets.QLabel("Subsequence Editing:")
        mainLayout.addWidget(subseqHeader)

        # Horizontal layout for Subsequence Entry
        subSeqLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(subSeqLayout)

        # Start Position LineEdit for Subsequence
        self.subStartPos = QtWidgets.QLineEdit()
        self.subStartPos.setPlaceholderText("Enter start nucleotide position for subsequence")
        self.subStartPos.setEnabled(False)  # Initially disabled
        subSeqLayout.addWidget(self.subStartPos)

        # End Position LineEdit for Subsequence
        self.subEndPos = QtWidgets.QLineEdit()
        self.subEndPos.setPlaceholderText("Enter end nucleotide position for subsequence")
        self.subEndPos.setEnabled(False)  # Initially disabled
        subSeqLayout.addWidget(self.subEndPos)

        # Nucleotide Position Button (Ok) for Subsequence
        self.NucPosButton = QtWidgets.QPushButton("Ok")
        self.NucPosButton.setEnabled(False)  # Initially disabled
        subSeqLayout.addWidget(self.NucPosButton)
        self.NucPosButton.clicked.connect(self.subSeqDisplay)

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

        # Go Button
        self.GoButton = QtWidgets.QPushButton("Go!")
        self.GoButton.setMaximumWidth(100)
        mainLayout.addWidget(self.GoButton, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.GoButton.clicked.connect(self.sequenceToProcess)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.UserSeqs = []
        self.observableRangeSet = False  # Track if observable range is set

        self.AddSeqButton.clicked.connect(self.addSequence)
        self.RemoveButton.clicked.connect(self.removeSequence)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Your Application"))
        self.AddSeqButton.setText(_translate("MainWindow", "Add Sequence"))
        self.RemoveButton.setText(_translate("MainWindow", "Remove Sequence"))
        self.tableWidget.setHorizontalHeaderLabels(["", "Sequence Name", "Sequence"])

    def saveObservableRange(self):
        chromosome = self.ChromosomeEdit.text().strip()
        obsStart = self.obsStartPos.text().strip()
        obsStop = self.obsEndPos.text().strip()

        if self.chromoConditions(chromosome) and self.obsStartStopConditions(obsStart, obsStop):
            self.chromoLabel.setText(f"Chromosome: {chromosome}")
            self.obsStartLabel.setText(f"Start Position: {obsStart}")
            self.obsStopLabel.setText(f"Stop Position: {obsStop}")
            self.observableRangeSet = True
            self.subStartPos.setEnabled(True)
            self.subEndPos.setEnabled(True)
            self.NucPosButton.setEnabled(True)
        else:
            self.observableRangeSet = False

    def subSeqDisplay(self):
        if not self.observableRangeSet:
            self.SeqErrors("Please set the observable range first.")
            return

        start_pos = self.subStartPos.text().strip()
        end_pos = self.subEndPos.text().strip()

        if self.obsStartStopConditions(start_pos, end_pos):
            subsequence = self.SeqEditor.text()[int(start_pos)-1:int(end_pos)]
            self.SeqEditor.setText(subsequence)
        else:
            self.SeqEditor.clear()

    def addSequence(self):
        sequence = self.SeqEditor.text()
        seqName = self.SeqName.text().strip()

        if self.SeqConditions(sequence, seqName):
            self.UserSeqs.append((sequence, seqName))
            self.updateTable()

    def removeSequence(self):
        selected_seq = self.getSelectedSequence()
        if selected_seq:
            self.UserSeqs.remove(selected_seq)
            self.updateTable()

    def getSelectedSequence(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        if len(selected_rows) != 1:
            self.SeqErrors("Please select one sequence.")
            return None

        row = selected_rows[0].row()
        selected_seq = (self.tableWidget.item(row, 0).text(), self.tableWidget.item(row, 1).text())
        return selected_seq

    def updateTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(self.UserSeqs))

        for row, (sequence, seqName) in enumerate(self.UserSeqs):
            item_sequence = QtWidgets.QTableWidgetItem(sequence)
            item_seqName = QtWidgets.QTableWidgetItem(seqName)

            self.tableWidget.setItem(row, 0, item_sequence)
            self.tableWidget.setItem(row, 1, item_seqName)

    def sequenceToProcess(self):
        selected_seq = self.getSelectedSequence()
        if selected_seq:
            self.SeqToProcess = selected_seq


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
