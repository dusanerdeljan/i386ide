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

from src.model.Node import Node, PathManager
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal, QObject
from PySide2.QtWidgets import QMenu, QAction, QMessageBox, QInputDialog, QLineEdit, QFileDialog
from src.view.NewFileDialog import NewFileDialog
from src.view.CompilerOptionsEditor import CompilerOptionsEditor
from src.model.AssemblyFileNode import AssemblyFileNode, AssemblyFileProxy
from src.model.CFileNode import CFileNode, CFileProxy
from src.model.FileNode import FileNode, FileProxy
import os
import re
import shutil
import main

class ProjectProxy(object):

    def __init__(self):
        self.path = None
        self.files = []
        self.parent = None
        self.gccOptions = ['-g', '-m32']

    def addFile(self, proxy):
        self.files.append(proxy)

    def getProjectPath(self):
        return os.path.join(self.parent.path, self.path)

    def getProjectCompileCommand(self):
        destination = os.path.join(self.getProjectPath(), "{}.out".format(self.path))
        cFiles = []
        sFiles = []
        for file in self.files:
            if isinstance(file, CFileProxy):
                cFiles.append(file.getFilePath())
            elif isinstance(file, AssemblyFileProxy):
                sFiles.append(file.getFilePath())
        command = ['gcc']
        command.extend(self.gccOptions)
        command.extend(['-o', destination])
        if cFiles:
            command.extend(cFiles)
        if sFiles:
            command.extend(sFiles)
        return ' '.join(command)

    def getProjectDebugCommand(self):
        return "ddd {}.out".format(os.path.join(self.getProjectPath(), self.path))

    def getProjectRunCommand(self):
        return "{}.out".format(os.path.join(self.getProjectPath(), self.path))

class ProjectNode(Node):

    def __init__(self):
        super(ProjectNode, self).__init__()
        self.eventManager = ProjectEventManager()
        self.menu = QMenu()
        self.menu.setStyleSheet("background-color: #3E3E42; color: white;")
        self.proxy = ProjectProxy()
        self.saveAction = QAction(QIcon(main.resource_path("resources/save_folder.png")), "Save project")
        self.deleteAction = QAction(QIcon(main.resource_path("resources/remove_folder.png")), "Remove project")
        self.eraseAction = QAction(QIcon(main.resource_path("resources/delete_folder.png")), "Delete project from disk")
        self.renameAction = QAction(QIcon(main.resource_path("resources/rename_folder.png")), "Rename project")
        self.compileAction = QAction(QIcon(main.resource_path("resources/compile.png")), "Compile project")
        self.runAction = QAction(QIcon(main.resource_path("resources/run.png")), "Run project")
        self.debugAction = QAction(QIcon(main.resource_path("resources/debug.png")), "Debug project")
        self.newFileAction = QAction(QIcon(main.resource_path("resources/new_file.png")), "New file")
        self.importFileAction = QAction(QIcon(main.resource_path("resources/import_file.png")), "Import file")
        self.compilerOptionsAction = QAction(QIcon(main.resource_path("resources/compiler_options.png")), "Compiler options")
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.compilerOptionsAction)
        self.menu.addAction(self.compileAction)
        self.menu.addAction(self.debugAction)
        self.menu.addAction(self.runAction)
        self.menu.addSeparator()
        self.menu.addAction(self.newFileAction)
        self.menu.addAction(self.importFileAction)
        self.menu.addSeparator()
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.deleteAction)
        self.menu.addAction(self.eraseAction)

        self.connectActions()

    def getContextMenu(self) -> QMenu:
        return self.menu

    def __str__(self):
        return self.proxy.path

    def connectFileEventHandlers(self, file: FileNode):
        file.eventManager.fileRemoveRequsted.connect(self.removeFile)
        file.eventManager.fileRename.connect(lambda oldPath, fileProxy: self.eventManager.fileRename.emit(oldPath, fileProxy))
        file.eventManager.fileSave.connect(lambda fileProxy: self.eventManager.fileSave.emit(fileProxy))
        file.eventManager.invalidFile.connect(self.detachFile)

    def connectActions(self):
        self.saveAction.triggered.connect(self.saveProject)
        self.newFileAction.triggered.connect(self.createNewFile)
        self.importFileAction.triggered.connect(self.importFile)
        self.deleteAction.triggered.connect(self.deleteProject)
        self.renameAction.triggered.connect(self.renameProject)
        self.compilerOptionsAction.triggered.connect(self.editCompilerOptions)
        self.eraseAction.triggered.connect(self.eraseActionTriggered)
        self.compileAction.triggered.connect(self.compileActionTriggered)
        self.debugAction.triggered.connect(self.debugActionTriggered)
        self.runAction.triggered.connect(self.runActionTriggered)

    def saveProject(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        self.eventManager.projectSave.emit(self.proxy)

    def detachFile(self, fileNode: FileNode):
        msg = QMessageBox()
        msg.setStyleSheet("background-color: #2D2D30; color: white;")
        msg.setModal(True)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("File '{}' has been deleted from the disk.".format(fileNode.proxy.path))
        msg.setWindowTitle("Invalid file")
        msg.exec_()
        self.proxy.files.remove(fileNode.proxy)
        self.removeChild(fileNode)
        self.parent().saveWorkspace()
        self.eventManager.fileRemove.emit(fileNode.proxy)

    def eraseActionTriggered(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        self.eventManager.projectDeleteFromDiskRequested.emit(self)

    def compileActionTriggered(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        self.eventManager.projectCompileRequested.emit(self.proxy)

    def debugActionTriggered(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        self.eventManager.projectDebugRequested.emit(self.proxy)

    def runActionTriggered(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        self.eventManager.projectRunRequested.emit(self.proxy)

    def editCompilerOptions(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        editor = CompilerOptionsEditor(self.proxy)
        if editor.exec_():
            self.parent().saveWorkspace()

    def renameProject(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        name, entered = QInputDialog.getText(None, "Rename project", "Enter new workspace name: ", QLineEdit.Normal, self.path)
        if entered:
            parentDir = os.path.abspath(os.path.join(self.proxy.getProjectPath(), os.pardir))
            newPath = os.path.join(parentDir, name)
            # print(newPath)
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
            if " " in name or regex.search(name):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Project name cannot contain whitespace or special characters.")
                msg.setWindowTitle("Project rename error")
                msg.exec_()
                return
            if os.path.exists(newPath):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Folder with the same name already exists.")
                msg.setWindowTitle("Project rename error")
                msg.exec_()
                return
            os.rename(self.path, newPath)
            oldPath = self.path
            self.proxy.path = self.path = os.path.basename(newPath)
            self.setText(0, self.path)
            self.parent().saveWorkspace()
            self.eventManager.projectRename.emit(oldPath, self)

    def removeFile(self, file: FileNode):
        answer = QMessageBox.question(None, "Delete file",
                                      "Are you sure you want to delete file {} from the disk?".format(file.proxy.path),
                                      QMessageBox.Yes | QMessageBox.No)
        if not answer == QMessageBox.Yes:
            return
        self.proxy.files.remove(file.proxy)
        os.remove(file.proxy.getFilePath())
        self.eventManager.fileRemove.emit(file.proxy)
        self.removeChild(file)
        self.parent().saveWorkspace()

    def importFile(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        name, entered = QFileDialog.getOpenFileName(None, "Select file to import", ".", "Assembly files (*.S);;C files (*.c)")
        if name:
            fileName = os.path.basename(name)
            filePath = os.path.join(self.proxy.getProjectPath(), fileName)
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
            if " " in filePath or regex.search(fileName):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("File name cannot contain whitespace or special characters.")
                msg.setWindowTitle("File import error")
                msg.exec_()
                return
            alreadyInProject = False
            inSameDir = False
            if os.path.exists(filePath):
                for proxy in self.proxy.files:
                    if proxy.getFilePath() == name:
                        alreadyInProject = True
                inSameDir = os.path.join(self.proxy.getProjectPath(), os.path.basename(filePath)) == name
                if alreadyInProject:
                    msg = QMessageBox()
                    msg.setStyleSheet("background-color: #2D2D30; color: white;")
                    msg.setModal(True)
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("File is already a part of the project.")
                    msg.setWindowTitle("File import error")
                    msg.exec_()
                    return
                if not inSameDir:
                    msg = QMessageBox()
                    msg.setStyleSheet("background-color: #2D2D30; color: white;")
                    msg.setModal(True)
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("File with the same name already exists.")
                    msg.setWindowTitle("File import error")
                    msg.exec_()
                    return
            node = None
            if fileName[-1] == "S":
                node = AssemblyFileNode()
                node.setIcon(0, QIcon(main.resource_path("resources/s.png")))
            else:
                node = CFileNode()
                node.setIcon(0, QIcon(main.resource_path("resources/c.png")))
            node.setText(0, fileName)
            node.path = fileName
            if isinstance(node, AssemblyFileNode):
                node.proxy = AssemblyFileProxy()
            elif isinstance(node, CFileNode):
                node.proxy = CFileProxy()
            node.proxy.path = fileName
            node.proxy.parent = self.proxy
            self.addChild(node)
            # if not inSameDir:
            #     os.mknod(filePath)
            self.proxy.addFile(node.proxy)
            self.connectFileEventHandlers(node)
            if not inSameDir:
                shutil.copyfile(name, filePath)
            self.setExpanded(True)
            # with open(filePath, 'w') as file:
            #     with open(name, 'r') as inputFile:
            #         file.write(inputFile.read())

    def createQuickAssemblyFile(self):
        fileName = self.path + ".S"
        node = AssemblyFileNode()
        node.setIcon(0, QIcon(main.resource_path("resources/s.png")))
        node.setText(0, fileName)
        node.path = fileName
        node.proxy = AssemblyFileProxy()
        node.proxy.path = fileName
        node.proxy.parent = self.proxy
        self.addChild(node)
        os.mknod(os.path.join(self.proxy.getProjectPath(), fileName))
        self.proxy.addFile(node.proxy)
        self.connectFileEventHandlers(node)
        self.setExpanded(True)
        return node

    def createNewFile(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        dialog = NewFileDialog()
        dialog.exec_()
        if dialog.result:
            rootPath = os.path.join(self.parent().path, self.path, dialog.result)
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
            if " " in dialog.result or regex.search(dialog.result):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("File name cannot contain whitespace or special characters.")
                msg.setWindowTitle("File creation error")
                msg.exec_()
                return
            if os.path.exists(rootPath):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("File with the same name already exists.")
                msg.setWindowTitle("File creation error")
                msg.exec_()
                return
            node = None
            if dialog.result[-1] == "S":
                node = AssemblyFileNode()
                node.setIcon(0, QIcon(main.resource_path("resources/s.png")))
            else:
                node = CFileNode()
                node.setIcon(0, QIcon(main.resource_path("resources/c.png")))
            node.setText(0, dialog.result)
            node.path = dialog.result
            if isinstance(node, AssemblyFileNode):
                node.proxy = AssemblyFileProxy()
            elif isinstance(node, CFileNode):
                node.proxy = CFileProxy()
            node.proxy.path = dialog.result
            node.proxy.parent = self.proxy
            self.addChild(node)
            os.mknod(rootPath)
            self.proxy.addFile(node.proxy)
            self.connectFileEventHandlers(node)
            self.setExpanded(True)


    def deleteProject(self):
        if not os.path.exists(self.proxy.getProjectPath()):
            self.eventManager.invalidProject.emit(self)
            return
        self.eventManager.projectRemoveRequested.emit(self)

    def loadProjectBackup(self):
        for proxy in self.proxy.files:
            node = None
            if isinstance(proxy, AssemblyFileProxy):
                node = AssemblyFileNode()
                node.setIcon(0, QIcon(main.resource_path("resources/s.png")))
            elif isinstance(proxy, CFileProxy):
                node = CFileNode()
                node.setIcon(0, QIcon(main.resource_path("resources/c.png")))
            if node:
                proxy.parent = self.proxy
                node.setText(0, proxy.path)
                node.path = proxy.path
                node.proxy = proxy
                try:
                    with open(proxy.getFilePath(), 'w') as file:
                        file.write(proxy.text)
                        proxy.hasUnsavedChanges = False
                except:
                    print("Could not write to file {}".format(proxy.getFilePath()))

                self.addChild(node)
                self.connectFileEventHandlers(node)


    def loadProject(self, sourcePath=None):
        toBeDeleted = []
        for proxy in self.proxy.files:
            file = None
            if os.path.exists(os.path.join(proxy.getFilePath())):
                if isinstance(proxy, AssemblyFileProxy):
                    file = AssemblyFileNode()
                    file.setIcon(0, QIcon(main.resource_path("resources/s.png")))
                elif isinstance(proxy, CFileProxy):
                    file = CFileNode()
                    file.setIcon(0, QIcon(main.resource_path("resources/c.png")))
                if file:
                    proxy.parent = self.proxy
                    file.setText(0, proxy.path)
                    file.path = proxy.path
                    file.proxy = proxy
                    self.addChild(file)
                    self.connectFileEventHandlers(file)
            else:
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText(
                    "Failed to import file '{}' because it is deleted from the disk.".format(proxy.path))
                msg.setWindowTitle("Failed to load a file.")
                msg.exec_()
                toBeDeleted.append(proxy)
        for proxy in toBeDeleted:
            self.proxy.files.remove(proxy)
        projectPath = self.proxy.getProjectPath() if not sourcePath else sourcePath
        for filePath in os.listdir(projectPath):
            if filePath not in [file.path for file in self.proxy.files]:
                node = None
                proxy = None
                if filePath.lower().endswith(".s"):
                    node = AssemblyFileNode()
                    node.setIcon(0, QIcon(main.resource_path("resources/s.png")))
                    proxy = AssemblyFileProxy()
                elif filePath.lower().endswith(".c"):
                    node = CFileNode()
                    node.setIcon(0, QIcon(main.resource_path("resources/c.png")))
                    proxy = CFileProxy()
                if node:
                    proxy.path = filePath
                    node.setText(0, filePath)
                    node.path = filePath
                    node.proxy = proxy
                    node.proxy.parent = self.proxy
                    self.addChild(node)
                    self.proxy.files.append(node.proxy)
                    self.connectFileEventHandlers(node)
                    if sourcePath:
                        shutil.copyfile(os.path.join(sourcePath, filePath), os.path.join(self.proxy.getProjectPath(), filePath))

class ProjectEventManager(QObject):

    projectCompileRequested = Signal(ProjectProxy)
    projectDebugRequested = Signal(ProjectProxy)
    projectRunRequested = Signal(ProjectProxy)
    projectRemoveRequested = Signal(ProjectNode)
    projectDeleteFromDiskRequested = Signal(ProjectNode)
    projectRename = Signal(str, ProjectNode)
    fileRemove = Signal(FileProxy)
    fileRename = Signal(str, FileProxy)
    fileSave = Signal(FileProxy)

    projectSave = Signal(ProjectProxy)

    invalidProject = Signal(ProjectNode)
    invalidFile = Signal(FileNode)

    def __init__(self):
        super(ProjectEventManager, self).__init__()


