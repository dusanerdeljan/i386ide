from PySide2.QtWidgets import QMenu, QAction
from src.model.Node import Node


class FileNode(Node):
    
    def __init__(self):
        super(FileNode, self).__init__()
        self.menu = QMenu()
        self.saveAction = QAction("Save file")
        self.renameAction = QAction("Rename file")
        self.deleteAction = QAction("Remove file")
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.deleteAction)

    def getContextMenu(self) -> QMenu:
        return self.menu