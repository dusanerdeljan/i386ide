from PySide2.QtGui import QIcon
from src.model.FileNode import FileNode, FileProxy


class AssemblyFileProxy(FileProxy):

    def __init__(self):
        super(AssemblyFileProxy, self).__init__()


class AssemblyFileNode(FileNode):
    
    def __init__(self):
        super(AssemblyFileNode, self).__init__()