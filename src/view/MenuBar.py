"""
    i386ide is lightweight IDE for i386 assembly and C programming language.
    Copyright (C) 2019  Dušan Erdeljan, Marko Njegomir

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

from PySide2.QtWidgets import QMenuBar, QAction, QMenu
from PySide2.QtGui import QKeySequence, QIcon
from src.controller.PathManager import PathManager
import os

class MenuBar(QMenuBar):

    def __init__(self):
        super(MenuBar, self).__init__()
        self.setStyleSheet("background-color: #2D2D30; color: white; font-weight: 500")
        self.file = self.addMenu("File")
        self.edit = self.addMenu("Edit")
        self.view = self.addMenu("View")
        # self.run = self.addMenu("Run")
        self.help = self.addMenu("Help")

        self.createFileMenuItemActions()
        self.createEditMenuItemActions()
        self.createViewMenuItemActions()

    def createFileMenuItemActions(self):
        self.newWorkspaceAction = QAction(QIcon(resource_path("resources/new_folder.png")), "New workspace", self)
        self.newWorkspaceAction.setShortcut(QKeySequence("Ctrl+N"))
        self.file.addAction(self.newWorkspaceAction)

        self.openWorkspaceAction = QAction(QIcon(resource_path("resources/open_folder.png")), "Open workspace", self)
        self.openWorkspaceAction.setShortcut(QKeySequence("Ctrl+O"))
        self.file.addAction(self.openWorkspaceAction)

        self.switchWorkspaceAction = QAction(QIcon(resource_path("resources/switch_folder.png")), "Switch workspace", self)
        self.switchWorkspaceAction.setShortcut((QKeySequence("Ctrl+W")))
        self.file.addAction(self.switchWorkspaceAction)

        self.saveWorkspaceAction = QAction(QIcon(resource_path("resources/save_folder.png")), "Save workspace", self)
        self.saveWorkspaceAction.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.file.addAction(self.saveWorkspaceAction)

        self.saveAction = QAction(QIcon(resource_path("resources/save_file.png")), "Save file", self)
        self.saveAction.setShortcut(QKeySequence("Ctrl+S"))
        self.file.addAction(self.saveAction)
        #
        # self.openAction = QAction("Open file", self)
        # self.openAction.setShortcut(QKeySequence("Ctrl+G"))
        # self.file.addAction(self.openAction)
        #
        # self.newAction = QAction("New file", self)
        # self.newAction.setShortcut(QKeySequence("Ctrl+F"))
        # self.file.addAction(self.newAction)

    def createEditMenuItemActions(self):
        self.editDefaultWorkspace = QAction(QIcon(resource_path("resources/workspace.png")), "Edit default workspace", self)
        self.edit.addAction(self.editDefaultWorkspace)

    def createViewMenuItemActions(self):
        self.showTerminal = QAction("Show terminal", self)
        self.view.addAction(self.showTerminal)

        self.hideTerminal = QAction("Hide terminal", self)
        self.view.addAction(self.hideTerminal)

        self.showTree = QAction("Show project explorer", self)
        self.view.addAction(self.showTree)

        self.hideTree = QAction("Hide project explorer", self)
        self.view.addAction(self.hideTree)

        self.showHelp = QAction("Show help", self)
        self.view.addAction(self.showHelp)

        self.hideHelp = QAction("Hide help", self)
        self.view.addAction(self.hideHelp)


from main import resource_path #mora ovde na kraju zbog nacina na koji python interpretira fajlove koji importuju jedan iz drugog