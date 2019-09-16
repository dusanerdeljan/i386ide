import pickle
import os
from src.model.WorkspaceNode import WorkspaceProxy

class WorkspaceConfiguration(object):

    USER  = os.getlogin()
    SAVE_FOLDER = os.path.join("/", "home", USER, ".i386ide")
    SAVE_PATH = os.path.join(SAVE_FOLDER, "settings.conf")

    def __init__(self):
        self.defaultWorkspace = None
        self.workspaces = set()

    def addWorkspace(self, workspace):
        self.workspaces.add(workspace)

    def getDefaultWorkspace(self):
        return self.defaultWorkspace

    def setDefaultWorkspace(self, workspace):
        self.defaultWorkspace = workspace

    def getWorkspaces(self):
        return self.workspaces

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
            return workspace
        except:
            return WorkspaceConfiguration()