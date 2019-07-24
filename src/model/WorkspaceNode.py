from PySide2.QtWidgets import QMenu, QAction
from src.model.Node import Node
from src.model.ProjectNode import ProjectNode


class WorkspaceNode(Node):
    
    def __init__(self):
        super(WorkspaceNode, self).__init__()
        self.menu = QMenu()
        self.newProjectAction = QAction("New project")
        self.saveAction = QAction("Save workspace")
        self.renameAction = QAction("Rename workspace")
        self.switchAction = QAction("Switch workspace")
        self.menu.addAction(self.newProjectAction)
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.switchAction)
        self.menu.addAction(self.renameAction)

        self.connectActions()

    def getContextMenu(self) -> QMenu:
        return self.menu

    def connectActions(self):
        item = ProjectNode()
        item.setText(0, "New project")
        self.newProjectAction.triggered.connect(lambda: self.addChild(item))