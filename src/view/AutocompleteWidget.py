from PySide2.QtWidgets import QListWidget, QListWidgetItem, QDialog, QVBoxLayout, QLabel
from PySide2.QtCore import Qt


class AutoCompleteListWidgetItem(QListWidgetItem):

    def __init__(self, text):
        super(AutoCompleteListWidgetItem, self).__init__()
        self.setText(text)

    def __str__(self):
        return self.text()


class AutocompleteWidget(QDialog):

    def __init__(self, suggestions: list):
        super(AutocompleteWidget, self).__init__()
        self.widget = QListWidget()
        self.widget.setStyleSheet("background-color: #232323;")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.vbox = QVBoxLayout()
        self.label = QLabel("")
        self.vbox.addWidget(self.widget, 10)
        self.vbox.addWidget(self.label, 1)
        self.setLayout(self.vbox)
        self.updateSuggestionList(suggestions)
        self.result = None

    def updateSuggestionList(self, suggestions):
        self.widget.clear()
        if suggestions:
            for keyword in suggestions:
                self.widget.addItem(AutoCompleteListWidgetItem(keyword))
            self.label.setText("Broj predloga: {}.".format(len(suggestions)))
        else:
            self.label.setText("Nema dostupnih predloga.")
        self.setSize()

    def setSize(self):
        self.setFixedSize(self.minimumSizeHint())
        self.setFixedWidth(300)


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_Return:
            selectedItems = self.widget.selectedItems()
            if len(selectedItems) > 0:
                self.result = selectedItems[0]
            self.close()
        if e.key() == Qt.Key_Backspace:
            self.close()
        if e.key() == Qt.Key_Left:
            self.parent().setFocus()