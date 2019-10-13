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

from PySide2.QtWidgets import QMenu, QAction, QMessageBox, QInputDialog, QLineEdit
from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QIcon
from src.model.Node import Node, PathManager
import os
import re
import main

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
        self.menu.setStyleSheet("background-color: #3E3E42; color: white;")
        self.eventManager = FileEventManager()
        self.proxy: FileProxy = None
        self.saveAction = QAction(QIcon(main.resource_path("resources/save_file.png")), "Save file")
        self.renameAction = QAction(QIcon(main.resource_path("resources/rename_file.png")), "Rename file")
        self.deleteAction = QAction(QIcon(main.resource_path("resources/delete_file.png")), "Delete file")
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.deleteAction)

        self.connectActions()

    def renameFile(self):
        if not os.path.exists(self.proxy.getFilePath()):
            self.eventManager.invalidFile.emit(self)
            return
        type = self.path.split(".")[1]
        name, entered = QInputDialog.getText(None, "Rename file", "Enter new file name: ", QLineEdit.Normal, self.path.split(".")[0])
        if entered:
            name += "."+type
            parentDir = os.path.abspath(os.path.join(self.proxy.getFilePath(), os.pardir))
            newPath = os.path.join(parentDir, name)
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
            if " " in name or regex.search(name):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("File name cannot contain whitespace or special characters.")
                msg.setWindowTitle("File rename error")
                msg.exec_()
                return
            if os.path.exists(newPath):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("File with the same name already exists.")
                msg.setWindowTitle("File rename error")
                msg.exec_()
                return
            os.rename(self.proxy.getFilePath(), newPath)
            oldPath = self.path
            self.proxy.path = self.path = os.path.basename(newPath)
            self.setText(0, self.path)
            self.eventManager.fileRename.emit(oldPath, self.proxy)


    def getContextMenu(self) -> QMenu:
        return self.menu

    def connectActions(self):
        self.deleteAction.triggered.connect(self.deleteActionTriggered)
        self.saveAction.triggered.connect(self.saveFile)
        self.renameAction.triggered.connect(self.renameFile)

    def deleteActionTriggered(self):
        if not os.path.exists(self.proxy.getFilePath()):
            self.eventManager.invalidFile.emit(self)
            return
        self.eventManager.fileRemoveRequsted.emit(self)

    def saveFile(self):
        if self.proxy.hasUnsavedChanges:
            try:
                self.proxy.saveFile()
                self.eventManager.fileSave.emit(self.proxy)
            except:
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("The following file could not be saved: {}".format(self.proxy.path))
                msg.setWindowTitle("File save error")
                msg.exec_()

    def getFilePath(self):
        return os.path.join(self.proxy.parent.parent.path, self.proxy.parent.path, self.proxy.path)
    
class FileEventManager(QObject):

    fileRemoveRequsted = Signal(FileNode)
    fileRename = Signal(str, FileProxy)
    fileSave = Signal(FileProxy)

    invalidFile = Signal(FileNode)

    def __init__(self):
        super(FileEventManager, self).__init__()
