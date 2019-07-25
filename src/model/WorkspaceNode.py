from PySide2.QtWidgets import QMenu, QAction, QInputDialog, QLineEdit
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
        self.newProjectAction.triggered.connect(self.createNewProject)

    def createNewProject(self):
        name, entered = QInputDialog.getText(None, "New project", "Enter project name: ", QLineEdit.Normal, "New project")
        if entered:
            project = ProjectNode()
            project.setText(0, name)
            self.addChild(project)