from src.model.Node import Node
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMenu, QAction


class ProjectNode(Node):

    def __init__(self):
        super(ProjectNode, self).__init__()
        self.menu = QMenu()
        self.saveAction = QAction("Save project")
        self.deleteAction = QAction("Remove project")
        self.renameAction = QAction("Rename project")
        self.compileAction = QAction("Compile project")
        self.runAction = QAction("Run project")
        self.newFileAction = QAction("New file")
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.compileAction)
        self.menu.addAction(self.runAction)
        self.menu.addSeparator()
        self.menu.addAction(self.newFileAction)
        self.menu.addSeparator()
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.deleteAction)

    def getContextMenu(self) -> QMenu:
        return self.menu
