from PySide2.QtWidgets import QMenu, QAction, QMessageBox
from src.model.Node import Node
import os


class FileProxy(object):

    def __init__(self):
        self.parent = None
        self.path = None
        self.text = None
        self.hasUnsavedChanges = False

    def getFilePath(self):
        return os.path.join(self.parent.parent.path, self.parent.path, self.path)


class FileNode(Node):
    
    def __init__(self):
        super(FileNode, self).__init__()
        self.menu = QMenu()
        self.proxy = None
        self.saveAction = QAction("Save file")
        self.renameAction = QAction("Rename file")
        self.deleteAction = QAction("Remove file")
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.deleteAction)

        self.connectActions()

    def getContextMenu(self) -> QMenu:
        return self.menu

    def connectActions(self):
        self.deleteAction.triggered.connect(self.deleteFile)

    def deleteFile(self):
        answer = QMessageBox.question(None, "Delete file",
                                      "Are you sure you want to delete file {}".format(self.text(0)),
                                      QMessageBox.Yes | QMessageBox.No)
        if not answer == QMessageBox.Yes:
            return
        self.parent().removeChild(self)
        del self

    def getFilePath(self):
        return os.path.join(self.proxy.parent.parent.path, self.proxy.parent.path, self.proxy.path)
