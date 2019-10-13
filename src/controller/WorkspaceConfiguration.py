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

import pickle
import os
import getpass
from src.model.WorkspaceNode import WorkspaceProxy

class WorkspaceConfiguration(object):

    USER = getpass.getuser()
    SAVE_FOLDER = os.path.join("/", "home", USER, ".i386ide")
    SAVE_PATH = os.path.join(SAVE_FOLDER, "settings.conf")

    def __init__(self):
        self.defaultWorkspace = None
        self.workspaces = []

    def addWorkspace(self, workspace):
        if workspace in self.workspaces:
            self.workspaces.remove(workspace)
        self.workspaces.insert(0, workspace)
        self.saveConfiguration()

    def removeWorkspace(self, workspace):
        self.workspaces.remove(workspace)
        if workspace == self.defaultWorkspace:
            self.defaultWorkspace = None
        self.saveConfiguration()

    def replaceWorkpsace(self, oldWorkspace, newWorkspace):
        self.workspaces.remove(oldWorkspace)
        self.workspaces.insert(0, newWorkspace)
        if self.defaultWorkspace == oldWorkspace:
            self.defaultWorkspace = newWorkspace
        self.saveConfiguration()

    def getDefaultWorkspace(self):
        return self.defaultWorkspace

    def setDefaultWorkspace(self, workspace):
        self.defaultWorkspace = workspace
        self.saveConfiguration()

    def getWorkspaces(self):
        return self.workspaces

    def setWorkspaces(self, workspaces):
        self.workspaces = workspaces

    def saveConfiguration(self):
        if not os.path.exists(WorkspaceConfiguration.SAVE_FOLDER):
            os.mkdir(WorkspaceConfiguration.SAVE_FOLDER)
        with open(self.SAVE_PATH, 'wb') as metadata:
            pickle.dump(self, metadata, protocol=pickle.HIGHEST_PROTOCOL)

    def clear(self):
        self.defaultWorkspace = None
        self.workspaces.clear()

    @staticmethod
    def loadConfiguration():
        try:
            with open(WorkspaceConfiguration.SAVE_PATH, 'rb') as file:
                workspace = pickle.load(file)
                if isinstance(workspace.getWorkspaces(), set):
                    lista = []
                    for ws in workspace.getWorkspaces():
                        lista.append(ws)
                    workspace.setWorkspaces(lista)
            return workspace
        except:
            return WorkspaceConfiguration()