from PySide2.QtWidgets import QListWidget, QTreeView


class TreeView(QListWidget):
    
    def __init__(self):
        super(TreeView, self).__init__()
        self.setStyleSheet("background-color: #44423E; color: white;")
        for i in range(20):
            self.addItem("Projekat{}.S".format(i))