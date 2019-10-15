"""
    i386ide is lightweight IDE for i386 assembly and C programming language.
    Copyright (C) 2019  Dušan Erdeljan, Marko Njegomir
    
    This file is part of i386ide.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from PySide2.QtWidgets import QMenu, QAction, QInputDialog, QLineEdit, QMessageBox, QFileDialog
from PySide2.QtCore import Signal, QObject
from PySide2.QtGui import QIcon
from src.model.Node import Node, PathManager
from src.model.ProjectNode import ProjectNode, ProjectProxy
from src.model.FileNode import FileProxy
import os
import pickle
import re
import shutil
import main

class WorkspaceProxy(object):

    def __init__(self):
        self.path = None
        self.projects = []
        self.closedNormally = True

    def addProject(self, projectProxy):
        self.projects.append(projectProxy)


class WorkspaceNode(Node):
    
    def __init__(self):
        super(WorkspaceNode, self).__init__()
        self.deleted = False
        self.eventManager = WorkspaceEventManager()
        self.menu = QMenu()
        self.menu.setStyleSheet("background-color: #3E3E42; color: white;")
        self.proxy = WorkspaceProxy()
        self.newProjectAction = QAction(QIcon(main.resource_path("resources/new_folder.png")), "New project")
        self.quickAssemblyProjectAction = QAction(QIcon(main.resource_path("resources/new_folder.png")), "Quick assembly project")
        self.importProjectAction = QAction(QIcon(main.resource_path("resources/open_folder.png")), "Import project")
        self.saveAction = QAction(QIcon(main.resource_path("resources/save_folder.png")), "Save workspace")
        self.renameAction = QAction(QIcon(main.resource_path("resources/rename_folder.png")), "Rename workspace")
        self.switchAction = QAction(QIcon(main.resource_path("resources/switch_folder.png")), "Switch workspace")
        self.updateAction = QAction(QIcon(main.resource_path("resources/update_folder.png")), "Update workspace")
        self.menu.addAction(self.newProjectAction)
        self.menu.addAction(self.quickAssemblyProjectAction)
        self.menu.addAction(self.importProjectAction)
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
        self.quickAssemblyProjectAction.triggered.connect(self.createQuickAssemblyProject)
        self.importProjectAction.triggered.connect(self.importProject)
        self.saveAction.triggered.connect(self.saveWorkspace)
        self.updateAction.triggered.connect(self.reloadWorkspace)

    def reloadWorkspace(self):
        if not os.path.exists(self.path):
            self.eventManager.invalidWorkspace.emit(self)
            return
        self.eventManager.workspaceReload.emit(self.proxy)

    def renameWorkspace(self):
        if not os.path.exists(self.path):
            self.eventManager.invalidWorkspace.emit(self)
            return
        name, entered = QInputDialog.getText(None, "Rename workspace", "Enter new workspace name: ", QLineEdit.Normal, os.path.basename(self.path))
        if entered:
            parentDir = os.path.abspath(os.path.join(self.path, os.pardir))
            newPath = os.path.join(parentDir, name)
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
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

    def importProject(self):
        if not os.path.exists(self.path):
            self.eventManager.invalidWorkspace.emit(self)
            return
        name = QFileDialog.getExistingDirectory(None, "Import project", ".", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if name:
            projectName = os.path.basename(name)
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
            if " " in name or regex.search(projectName):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Project name cannot contain whitespace or special characters.")
                msg.setWindowTitle("Project import error")
                msg.exec_()
                return
            if os.path.exists(os.path.join(self.path, projectName)) and os.path.join(self.path, projectName) != name:
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Folder with the same name already exists.")
                msg.setWindowTitle("Project import error")
                msg.exec_()
                return
            for projectProxy in self.proxy.projects:
                if projectProxy.getProjectPath() == name:
                    msg = QMessageBox()
                    msg.setStyleSheet("background-color: #2D2D30; color: white;")
                    msg.setModal(True)
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Project is already a part of the workspace.")
                    msg.setWindowTitle("Project import error")
                    msg.exec_()
                    return
            project = ProjectNode()
            project.path = projectName
            project.proxy.path = projectName
            project.proxy.parent = self.proxy
            project.setIcon(0, QIcon(main.resource_path("resources/project.png")))
            project.setText(0, projectName)
            self.addChild(project)
            newPath = os.path.join(self.path, projectName)
            if os.path.join(self.path, projectName) != name:
                os.mkdir(newPath)
            self.proxy.addProject(project.proxy)
            sourcePath = name if os.path.join(self.path, projectName) != name else None
            project.loadProject(sourcePath)
            self.saveWorkspace()
            self.connectProjectEventHandlers(project)
            self.eventManager.projectAdded.emit(project)

    def createQuickAssemblyProject(self):
        project = self.createNewProject(quickAssembly=True)
        if not project:
            return
        fileNode = project.createQuickAssemblyFile()
        self.eventManager.quickAssemblyFile.emit(fileNode.proxy)

    def createNewProject(self, quickAssembly=False):
        if not os.path.exists(self.path):
            self.eventManager.invalidWorkspace.emit(self)
            return
        dialogText = "New assembly project" if quickAssembly else "New project"
        name, entered = QInputDialog.getText(None, dialogText, "Enter project name: ", QLineEdit.Normal, "New project")
        if entered:
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
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
            project.setIcon(0, QIcon(main.resource_path("resources/project.png")))
            project.setText(0, name)
            self.addChild(project)
            newPath = os.path.join(self.path, name)
            os.mkdir(newPath)
            self.proxy.addProject(project.proxy)
            self.saveWorkspace()
            self.connectProjectEventHandlers(project)
            self.eventManager.projectAdded.emit(project)
            return project

    def saveBackup(self, ws_path=None):
        try:
            previous_state = self.proxy.closedNormally
        except:
            self.proxy.closedNormally = True
            previous_state = self.proxy.closedNormally
        self.proxy.closedNormally = True
        if ws_path:
            save_path = ws_path
        else:
            save_path = self.proxy.path
        try:
            with open(os.path.join(save_path, '.backup'), 'wb') as backup:
                pickle.dump(self.proxy, backup, protocol=pickle.HIGHEST_PROTOCOL)
        except:
            return
        self.proxy.closedNormally = previous_state

    def saveWorkspace(self, ws_path=None):
        if not os.path.exists(self.path):
            self.eventManager.invalidWorkspace.emit(self)
            return
        try:
           test = self.proxy.closedNormally
        except:
            self.proxy.closedNormally = True
        if ws_path:
            save_path = ws_path
        else:
            save_path = self.proxy.path
        try:
            with open(os.path.join(save_path, '.metadata'), 'wb') as metadata:
                pickle.dump(self.proxy, metadata, protocol=pickle.HIGHEST_PROTOCOL)
        except:
            return
        self.saveBackup(save_path)


    def connectProjectEventHandlers(self, project: ProjectNode):
        project.eventManager.projectCompileRequested.connect(lambda proxy: self.eventManager.projectCompile.emit(proxy))
        project.eventManager.projectDebugRequested.connect(lambda proxy: self.eventManager.projectDebug.emit(proxy))
        project.eventManager.projectRunRequested.connect(lambda proxy: self.eventManager.projectRun.emit(proxy))
        project.eventManager.projectRemoveRequested.connect(self.removeProject)
        project.eventManager.projectDeleteFromDiskRequested.connect(self.deleteProjectFromDisk)
        project.eventManager.projectRename.connect(lambda oldPath, project: self.eventManager.projectRename.emit(oldPath, project))
        project.eventManager.fileRemove.connect(lambda fileProxy: self.eventManager.fileRemove.emit(fileProxy))
        project.eventManager.fileRename.connect(lambda oldPath, fileProxy: self.renameFile(oldPath, fileProxy))
        project.eventManager.fileSave.connect(lambda fileProxy: self.eventManager.fileSave.emit(fileProxy))
        project.eventManager.invalidProject.connect(lambda projectNode: self.removeProject(projectNode, ask=False))
        project.eventManager.projectSave.connect(lambda projectProxy: self.eventManager.projectSave.emit(projectProxy))

    def renameFile(self, oldPath, fileProxy):
        self.saveWorkspace()
        self.eventManager.fileRename.emit(oldPath, fileProxy)

    def removeProject(self, project: ProjectNode, ask=True):
        if ask:
            answer = QMessageBox.question(None, "Delete project",
                                          "Are you sure you want to remove project {} from the workspace?".format(project.proxy.path),
                                          QMessageBox.Yes | QMessageBox.No)
            if not answer == QMessageBox.Yes:
                return
        else:
            msg = QMessageBox()
            msg.setStyleSheet("background-color: #2D2D30; color: white;")
            msg.setModal(True)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Project '{}' has been deleted from the disk.".format(project.proxy.path))
            msg.setWindowTitle("Invalid project")
            msg.exec_()
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

    def loadBackupWorkspace(self, ws_path=None):
        for projectProxy in self.proxy.projects:
            projectProxy.parent = self.proxy
            project = ProjectNode()
            project.setIcon(0, QIcon(main.resource_path("resources/project.png")))
            project.setText(0, projectProxy.path)
            project.path = projectProxy.path
            project.proxy = projectProxy
            project.loadProjectBackup()
            self.addChild(project)
            self.connectProjectEventHandlers(project)
        return True

    def loadWorkspace(self):
        toBeDeleted = []

        for projectProxy in self.proxy.projects:
            if os.path.exists(projectProxy.getProjectPath()):
                projectProxy.parent = self.proxy
                project = ProjectNode()
                project.setIcon(0, QIcon(main.resource_path("resources/project.png")))
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

    projectSave = Signal(ProjectProxy)

    fileRemove = Signal(FileProxy)
    fileRename = Signal(str, FileProxy)
    fileSave = Signal(FileProxy)

    quickAssemblyFile = Signal(FileProxy)

    invalidWorkspace = Signal(WorkspaceNode)

    def __init__(self):
        super(WorkspaceEventManager, self).__init__()