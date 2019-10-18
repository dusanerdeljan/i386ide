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

from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction, QLabel, QMessageBox
from PySide2.QtCore import Qt, Signal
from src.model.WorkspaceNode import WorkspaceNode, WorkspaceProxy
from src.model.FileNode import FileNode, FileProxy
from src.model.ProjectNode import ProjectNode, ProjectProxy
from src.controller.ConfigurationManager import ConfigurationManager
import os

class TreeView(QTreeWidget):

    fileDoubleCliked = Signal(FileProxy)
    newProjectAdded = Signal(ProjectNode)
    workspaceReload = Signal(WorkspaceProxy)
    workspaceRename = Signal(str, WorkspaceProxy)

    projectCompile = Signal(ProjectProxy)
    projectDebug = Signal(ProjectProxy)
    projectRun = Signal(ProjectProxy)
    projectRemove = Signal(ProjectProxy)
    projectRename = Signal(str, ProjectNode)

    projectSave = Signal(ProjectProxy)

    fileRemove = Signal(FileProxy)
    fileRename = Signal(str, FileProxy)
    fileSave = Signal(FileProxy)
    newFile = Signal(FileProxy)

    quickAssemblyFile = Signal(FileProxy)

    invalidWorkspace = Signal(WorkspaceNode)
    
    def __init__(self, configurationManager: ConfigurationManager):
        super(TreeView, self).__init__()
        self.configurationManager = configurationManager
        self.setRootIsDecorated(False)
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.rootNode: WorkspaceNode = None
        self.setAcceptDrops(True)

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if not item:
            return
        super(TreeView, self).mouseDoubleClickEvent(event)
        if isinstance(item, FileNode):
            if not os.path.exists(item.proxy.getFilePath()):
                item.eventManager.invalidFile.emit(item)
            else:
                self.fileDoubleCliked.emit(item.proxy)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if not os.path.exists(self.rootNode.path):
            self.rootNode.eventManager.invalidWorkspace.emit(self.rootNode)
            return
        mimeData = event.mimeData()
        position = event.pos()
        dropDestItem = self.itemAt(position)
        if not mimeData.hasUrls():
            return
        urls = mimeData.urls()
        if dropDestItem and isinstance(dropDestItem, ProjectNode):
            for i in range(len(urls)):
                fileUrl = urls[i].toLocalFile()
                if fileUrl.endswith(".S") and os.path.isfile(fileUrl):
                    dropDestItem.importFile(fileUrl)
        elif dropDestItem and isinstance(dropDestItem, FileNode):
            project = dropDestItem.parent()
            for i in range(len(urls)):
                fileUrl = urls[i].toLocalFile()
                if fileUrl.endswith(".S") and os.path.isfile(fileUrl):
                    project.importFile(fileUrl)
        else:
            if len(urls) == 1:
                folderPath = urls[0].toLocalFile()
                if os.path.isdir(folderPath):
                    self.rootNode.importProject(folderPath)
                    self.rootNode.saveWorkspace()
                    return
            answer = QMessageBox.question(None, "Import file(s)", "Do you want to create a project?", QMessageBox.Yes | QMessageBox.No)
            if not answer == QMessageBox.Yes:
                return
            validUrls = []
            for i in range(len(urls)):
                url = urls[i].toLocalFile()
                if url.endswith(".S") or url.endswith(".c"):
                    if os.path.isfile(url):
                        validUrls.append(url)
            if len(validUrls) == 0:
                return
            projectName = validUrls[0][:-2] if len(validUrls) == 1 else "Project"
            projectPath = os.path.join(self.rootNode.path, projectName)
            while os.path.exists(projectPath):
                projectName += "_1"
                projectPath = os.path.join(self.rootNode.path, projectName)
            projectNode = self.rootNode.createNewProject(path=projectPath)
            for fileUrl in validUrls:
                projectNode.importFile(fileUrl)
        self.rootNode.saveWorkspace()
        event.acceptProposedAction()


    def showContextMenu(self, pos):
        item = self.itemAt(pos)
        if not item:
            if self.rootNode:
                self.rootNode.getContextMenu().exec_(self.viewport().mapToGlobal(pos))
            return
        menu = item.getContextMenu()
        if menu:
            menu.exec_(self.viewport().mapToGlobal(pos))


    def addNode(self, parent: QTreeWidgetItem, item: QTreeWidgetItem):
        parent.addChild(item)

    def getProjects(self):
        children = []
        if self.rootNode:
            for childIndex in range(0, self.rootNode.childCount()):
                children.append(self.rootNode.child(childIndex))
        return children

    def newProject(self, project: ProjectNode):
        project.setExpanded(True)
        self.configurationManager.allProjects.append(project)
        self.newProjectAdded.emit(project)

    def removeProject(self, project: ProjectNode):
        self.configurationManager.allProjects = []
        for proj in self.getProjects():
            if proj is not project:
                self.configurationManager.allProjects.append(proj)
        self.projectRemove.emit(project.proxy)

    def renameProject(self, oldPath, project: ProjectNode):
        self.projectRename.emit(oldPath, project)

    def connectWorkspaceEventHandlers(self):
        self.rootNode.eventManager.projectAdded.connect(self.newProject)
        self.rootNode.eventManager.projectCompile.connect(lambda proxy: self.projectCompile.emit(proxy))
        self.rootNode.eventManager.projectDebug.connect(lambda proxy: self.projectDebug.emit(proxy))
        self.rootNode.eventManager.projectRun.connect(lambda proxy: self.projectRun.emit(proxy))
        self.rootNode.eventManager.projectRemove.connect(self.removeProject)
        self.rootNode.eventManager.projectRename.connect(self.renameProject)
        self.rootNode.eventManager.workspaceReload.connect(lambda wsProxy: self.workspaceReload.emit(wsProxy))
        self.rootNode.eventManager.workspaceRename.connect(lambda oldPath, wsProxy: self.workspaceRename.emit(oldPath, wsProxy))
        self.rootNode.eventManager.fileRemove.connect(lambda fileProxy: self.fileRemove.emit(fileProxy))
        self.rootNode.eventManager.fileRename.connect(lambda oldPath, fileProxy: self.fileRename.emit(oldPath, fileProxy))
        self.rootNode.eventManager.fileSave.connect(lambda fileProxy: self.fileSave.emit(fileProxy))
        self.rootNode.eventManager.invalidWorkspace.connect(lambda workspace: self.invalidWorkspace.emit(workspace))
        self.rootNode.eventManager.projectSave.connect(lambda projectProxy: self.projectSave.emit(projectProxy))
        self.rootNode.eventManager.quickAssemblyFile.connect(lambda fileProxy: self.quickAssemblyFile.emit(fileProxy))
        self.rootNode.eventManager.newFile.connect(lambda fileProxy: self.newFile.emit(fileProxy))

    def setRoot(self, item: QTreeWidgetItem):
        self.clear()
        self.rootNode = item
        self.addTopLevelItem(item)
        self.connectWorkspaceEventHandlers()
        item.setExpanded(True)