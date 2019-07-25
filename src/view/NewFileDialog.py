from PySide2.QtWidgets import QDialog, QComboBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout


class NewFileDialog(QDialog):
    
    def __init__(self):
        super(NewFileDialog, self).__init__()
        self.comboBox = QComboBox()
        self.comboBox.addItem("Assembly file")
        self.comboBox.addItem("C file")
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Enter file name...")
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.create = QPushButton("Create")
        self.cancel = QPushButton("Cancel")
        self.setWindowTitle("New file")
        self.result = None
        self.initGUI()

    def initGUI(self):
        self.vbox.addWidget(self.lineEdit)
        self.vbox.addWidget(self.comboBox)
        self.hbox.addWidget(self.create)
        self.hbox.addWidget(self.cancel)
        self.create.setDefault(True)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        self.setFixedSize(self.sizeHint())

        self.create.clicked.connect(self.createButtonClicked)
        self.cancel.clicked.connect(self.cancelButtonClicked)

    def createButtonClicked(self):
        extension = ".S" if self.comboBox.currentIndex() == 0 else ".c"
        self.result = "{}{}".format(self.lineEdit.text().strip(), extension)
        self.close()

    def cancelButtonClicked(self):
        self.result = None
        self.close()