from PySide2.QtWidgets import QMenu, QAction, QInputDialog, QLineEdit, QMessageBox
from PySide2.QtCore import Signal, QObject
from src.model.Node import Node
from src.model.ProjectNode import ProjectNode, ProjectProxy
import os
import pickle


class WorkspaceProxy(object):

    def __init__(self):
        self.path = None
        self.projects = []

    def addProject(self, projectProxy):
        self.projects.append(projectProxy)


class WorkspaceEventManager(QObject):

    projectAdded = Signal(ProjectNode)

    def __init__(self):
        super(WorkspaceEventManager, self).__init__()


class WorkspaceNode(Node):
    
    def __init__(self):
        super(WorkspaceNode, self).__init__()
        self.eventManager = WorkspaceEventManager()
        self.menu = QMenu()
        self.proxy = WorkspaceProxy()
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
        self.saveAction.triggered.connect(self.saveWorkspace)

    def createNewProject(self):
        name, entered = QInputDialog.getText(None, "New project", "Enter project name: ", QLineEdit.Normal, "New project")
        if entered:
            if os.path.exists(os.path.join(self.path, name)):
                msg = QMessageBox()
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Folder with the same name already exists.")
                msg.setWindowTitle("Project creation error")
                msg.exec_()
                return
            project = ProjectNode()
            project.path = name
            project.proxy.path = name
            project.proxy.parent = self.proxy
            project.setText(0, name)
            self.addChild(project)
            newPath = os.path.join(self.path, name)
            os.mkdir(newPath)
            self.proxy.addProject(project.proxy)
            self.saveWorkspace()
            self.eventManager.projectAdded.emit(project)

    def saveWorkspace(self):
        with open(os.path.join(self.path, '.metadata'), 'wb') as metadata:
            pickle.dump(self.proxy, metadata, protocol=pickle.HIGHEST_PROTOCOL)

    def loadWorkspace(self):
        toBeDeleted = []
        for projectProxy in self.proxy.projects:
            if os.path.exists(projectProxy.getProjectPath()):
                projectProxy.parent = self.proxy
                project = ProjectNode()
                project.setText(0, projectProxy.path)
                project.path = projectProxy.path
                project.proxy = projectProxy
                project.loadProject()
                self.addChild(project)
            else:
                msg = QMessageBox()
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Failed to import project '{}' because it is deleted from the disk.".format(projectProxy.path))
                msg.setWindowTitle("Failed to load a project.")
                msg.exec_()
                toBeDeleted.append(projectProxy)
        for proxy in toBeDeleted:
            self.proxy.projects.remove(proxy)
        self.saveWorkspace()