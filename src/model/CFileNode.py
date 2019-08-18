from PySide2.QtGui import QIcon
from src.model.FileNode import FileNode, FileProxy


class CFileProxy(FileProxy):

    def __init__(self):
        super(CFileProxy, self).__init__()


class CFileNode(FileNode):
    
    def __init__(self):
        super(CFileNode, self).__init__()