from PySide2.QtWidgets import QMenu, QAction, QInputDialog, QLineEdit, QMessageBox
from PySide2.QtCore import Signal, QObject
from PySide2.QtGui import QIcon
from src.model.Node import Node
from src.model.ProjectNode import ProjectNode, ProjectProxy
from src.model.FileNode import FileProxy
import os
import pickle
import re
import shutil


class WorkspaceProxy(object):

    def __init__(self):
        self.path = None
        self.projects = []

    def addProject(self, projectProxy):
        self.projects.append(projectProxy)


class WorkspaceEventManager(QObject):

    projectAdded = Signal(ProjectNode)
    workspaceReload = Signal(WorkspaceProxy)
    workspaceRename = Signal(str, WorkspaceProxy)

    projectCompile = Signal(ProjectProxy)
    projectDebug = Signal(ProjectProxy)
    projectRun = Signal(ProjectProxy)
    projectRemove = Signal(ProjectNode)
    projectDeleteFromDisk = Signal(ProjectNode)
    projectRename = Signal(str, ProjectNode)

    fileRemove = Signal(FileProxy)
    fileRename = Signal(str, FileProxy)

    def __init__(self):
        super(WorkspaceEventManager, self).__init__()


class WorkspaceNode(Node):
    
    def __init__(self):
        super(WorkspaceNode, self).__init__()
        self.eventManager = WorkspaceEventManager()
        self.menu = QMenu()
        self.menu.setStyleSheet("background-color: #3E3E42; color: white;")
        self.proxy = WorkspaceProxy()
        self.newProjectAction = QAction(QIcon("resources/new_folder.png"), "New project")
        self.saveAction = QAction(QIcon("resources/save_folder.png"), "Save workspace")
        self.renameAction = QAction(QIcon("resources/rename_folder.png"), "Rename workspace")
        self.switchAction = QAction(QIcon("resources/switch_folder.png"), "Switch workspace")
        self.updateAction = QAction(QIcon("resources/update_folder.png"), "Update workspace")
        self.menu.addAction(self.newProjectAction)
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.switchAction)
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.updateAction)

        self.connectActions()

    def getContextMenu(self) -> QMenu:
        return self.menu

    def connectActions(self):
        self.renameAction.triggered.connect(self.renameWorkspace)
        self.newProjectAction.triggered.connect(self.createNewProject)
        self.saveAction.triggered.connect(self.saveWorkspace)
        self.updateAction.triggered.connect(lambda: self.eventManager.workspaceReload.emit(self.proxy))

    def renameWorkspace(self):
        name, entered = QInputDialog.getText(None, "Rename workspace", "Enter new workspace name: ", QLineEdit.Normal, os.path.basename(self.path))
        if entered:
            parentDir = os.path.abspath(os.path.join(self.path, os.pardir))
            newPath = os.path.join(parentDir, name)
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if " " in name or regex.search(name):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Workspace name cannot contain whitespace or special characters.")
                msg.setWindowTitle("Workspace rename error")
                msg.exec_()
                return
            if os.path.exists(newPath):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Folder with the same name already exists.")
                msg.setWindowTitle("Workspace rename error")
                msg.exec_()
                return
            os.rename(self.path, newPath)
            oldPath = self.path
            self.proxy.path = self.path = newPath
            self.setText(0, os.path.basename(self.path))
            self.saveWorkspace()
            self.eventManager.workspaceRename.emit(oldPath, self.proxy)

    def createNewProject(self):
        name, entered = QInputDialog.getText(None, "New project", "Enter project name: ", QLineEdit.Normal, "New project")
        if entered:
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if " " in name or regex.search(name):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Project name cannot contain whitespace or special characters.")
                msg.setWindowTitle("Project creation error")
                msg.exec_()
                return
            if os.path.exists(os.path.join(self.path, name)):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
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
            project.setIcon(0, QIcon("resources/project.png"))
            project.setText(0, name)
            self.addChild(project)
            newPath = os.path.join(self.path, name)
            os.mkdir(newPath)
            self.proxy.addProject(project.proxy)
            self.saveWorkspace()
            self.connectProjectEventHandlers(project)
            self.eventManager.projectAdded.emit(project)

    def saveWorkspace(self):
        with open(os.path.join(self.path, '.metadata'), 'wb') as metadata:
            pickle.dump(self.proxy, metadata, protocol=pickle.HIGHEST_PROTOCOL)

    def connectProjectEventHandlers(self, project: ProjectNode):
        project.eventManager.projectCompileRequested.connect(lambda proxy: self.eventManager.projectCompile.emit(proxy))
        project.eventManager.projectDebugRequested.connect(lambda proxy: self.eventManager.projectDebug.emit(proxy))
        project.eventManager.projectRunRequested.connect(lambda proxy: self.eventManager.projectRun.emit(proxy))
        project.eventManager.projectRemoveRequested.connect(self.removeProject)
        project.eventManager.projectDeleteFromDiskRequested.connect(self.deleteProjectFromDisk)
        project.eventManager.projectRename.connect(lambda oldPath, project: self.eventManager.projectRename.emit(oldPath, project))
        project.eventManager.fileRemove.connect(lambda fileProxy: self.eventManager.fileRemove.emit(fileProxy))
        project.eventManager.fileRename.connect(lambda oldPath, fileProxy: self.renameFile(oldPath, fileProxy))

    def renameFile(self, oldPath, fileProxy):
        self.saveWorkspace()
        self.eventManager.fileRename.emit(oldPath, fileProxy)

    def removeProject(self, project: ProjectNode):
        answer = QMessageBox.question(None, "Delete project",
                                      "Are you sure you want to remove project {} from the workspace?".format(project.proxy.path),
                                      QMessageBox.Yes | QMessageBox.No)
        if not answer == QMessageBox.Yes:
            return
        self.proxy.projects.remove(project.proxy)
        self.eventManager.projectRemove.emit(project)
        self.removeChild(project)
        self.saveWorkspace()

    def deleteProjectFromDisk(self, project: ProjectNode):
        answer = QMessageBox.question(None, "Delete project from disk",
                                      "Are you sure you want to delete project {} and all its content from the disk?".format(
                                          project.proxy.path),
                                      QMessageBox.Yes | QMessageBox.No)
        if not answer == QMessageBox.Yes:
            return
        self.proxy.projects.remove(project.proxy)
        shutil.rmtree(project.proxy.getProjectPath())
        self.eventManager.projectRemove.emit(project)
        self.removeChild(project)
        self.saveWorkspace()

    def loadWorkspace(self):
        toBeDeleted = []
        for projectProxy in self.proxy.projects:
            if os.path.exists(projectProxy.getProjectPath()):
                projectProxy.parent = self.proxy
                project = ProjectNode()
                project.setIcon(0, QIcon("resources/project.png"))
                project.setText(0, projectProxy.path)
                project.path = projectProxy.path
                project.proxy = projectProxy
                project.loadProject()
                self.addChild(project)
                self.connectProjectEventHandlers(project)
            else:
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Failed to import project '{}' because it is deleted from the disk.".format(projectProxy.path))
                msg.setWindowTitle("Failed to load a project.")
                msg.exec_()
                toBeDeleted.append(projectProxy)
        for proxy in toBeDeleted:
            self.proxy.projects.remove(proxy)
        try:
            self.saveWorkspace()
            return True
        except:
            return False