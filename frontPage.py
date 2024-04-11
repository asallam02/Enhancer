import sys
from PyQt6 import QtCore, QtGui, QtWidgets

from Models.Backend.Query import Query
from Models.Backend.Enformer import Enformer

class MainPage(QtWidgets.QWidget):
    MODEL = None ##PLEASE ADD ENFORMER MODEL PASSED FROM MAIN HERE
    selectedIdx = -1


    def __init__(self, model, parent=None):
        self.model = model
        super().__init__(parent)
        self.UserSeqs = []
        self.QueryObjects = []
        self.tempQuery = None

        mainLayout = QtWidgets.QVBoxLayout(self)

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
        subSeqLayout.addWidget(self.subStartPos)

        # End Position LineEdit for Subsequence
        self.subEndPos = QtWidgets.QLineEdit()
        self.subEndPos.setPlaceholderText("Enter end nucleotide position for subsequence")
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

        self.retranslateUi()
        self.AddSeqButton.clicked.connect(self.addSequence)
        self.RemoveButton.clicked.connect(self.removeSequence)

    def retranslateUi(self):
        self.setWindowTitle("Sequence Widget")
        self.AddSeqButton.setText("Add Sequence")
        self.RemoveButton.setText("Remove Sequence")
        self.tableWidget.setHorizontalHeaderLabels(["", "Sequence Name", "Sequence"])

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

    def saveObservableRange(self):
        chromosome = self.ChromosomeEdit.text()
        obsStart = int(self.obsStartPos.text())
        obsStop = int(self.obsEndPos.text())

        if self.chromoConditions(chromosome) and self.obsStartStopConditions(obsStart, obsStop):
            self.chromoLabel.setText(f"Chromosome: {chromosome}")
            self.obsStartLabel.setText(f"Start Position: {obsStart}")
            self.obsStopLabel.setText(f"Stop Position: {obsStop}")
            self.observableRangeSet = True
            self.subStartPos.setEnabled(True)
            self.subEndPos.setEnabled(True)
            self.NucPosButton.setEnabled(True)

            #MAKE QUEREY OBJECT HERE
            self.tempQuery = Query(chromosome, obsStart, obsStop, self.MODEL)
        else:
            self.observableRangeSet = False


    def subSeqDisplay(self):
        if not self.observableRangeSet:
            self.SeqErrors("Please set the observable range first.")
            return
        
        startSubSeq = int(self.subStartPos.text())
        endSubSeq = int(self.subEndPos.text())

        if not self.obsStartStopConditions(startSubSeq, endSubSeq):
            return

        subSeq = self.tempQuery.define_sub_seq(startSubSeq, endSubSeq)
        self.SeqEditor.setText(subSeq)
        self.SeqEditor.setReadOnly(False)

    def addSequence(self):
        sequence = self.SeqEditor.text()
        seqName = self.SeqName.text()

        if not self.SeqConditions(sequence, seqName):
            return
        self.UserSeqs.append((sequence, seqName))
        self.updateTable()

        self.tempQuery.update_sub_seq(sequence)
        self.QueryObjects.append(self.tempQuery)

        #reset variable so it can't be changed
        self.tempQuery = None

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
            del self.QueryObjects[row]
        self.updateTable()

    def sequenceToProcess(self):
        selected_rowsProcess = [index for index in range(self.tableWidget.rowCount()) if self.tableWidget.item(index, 0).checkState() == QtCore.Qt.CheckState.Checked]
        if len(selected_rowsProcess) != 1:
            self.SeqErrors("Please select one sequence.")
            return

        seqNametoProcess = self.tableWidget.item(selected_rowsProcess[0], 1).text()
        sequencetoProcess = self.tableWidget.item(selected_rowsProcess[0], 2).text()

        # Save the selected sequence name and sequence to SeqToProcess
        self.SeqToProcess = (seqNametoProcess, sequencetoProcess)
        self.QueryToProcess = self.QueryObjects[selected_rowsProcess[0]]

        # Proceed with further processing or display the selected sequence
        print(f"Selected sequence name: {seqNametoProcess}, Sequence: {sequencetoProcess}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    model = Enformer()
    widget = MainPage(model)
    widget.show()
    sys.exit(app.exec())