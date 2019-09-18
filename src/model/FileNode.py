from PySide2.QtWidgets import QMenu, QAction, QMessageBox
from PySide2.QtCore import QObject, Signal
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

    def saveFile(self):
        with open(self.getFilePath(), 'w') as file:
            file.write(self.text)
            self.hasUnsavedChanges = False


class FileNode(Node):
    
    def __init__(self):
        super(FileNode, self).__init__()
        self.menu = QMenu()
        self.eventManager = FileEventManager()
        self.proxy: FileProxy = None
        self.saveAction = QAction("Save file")
        self.renameAction = QAction("Rename file")
        self.deleteAction = QAction("Delete file")
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.deleteAction)

        self.connectActions()

    def getContextMenu(self) -> QMenu:
        return self.menu

    def connectActions(self):
        self.deleteAction.triggered.connect(lambda: self.eventManager.fileRemoveRequsted.emit(self))
        self.saveAction.triggered.connect(self.saveFile)

    def saveFile(self):
        self.proxy.saveFile()

    def getFilePath(self):
        return os.path.join(self.proxy.parent.parent.path, self.proxy.parent.path, self.proxy.path)
    
class FileEventManager(QObject):

    fileRemoveRequsted = Signal(FileNode)

    def __init__(self):
        super(FileEventManager, self).__init__()
