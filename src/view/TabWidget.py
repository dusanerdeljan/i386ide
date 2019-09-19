from PySide2.QtWidgets import QTabWidget, QWidget, QMessageBox
from src.view.CodeEditor import CodeEditor
from src.model.FileNode import FileProxy

class EditorTab(QWidget):
    
    def __init__(self, fileProxy: FileProxy):
        super(EditorTab, self).__init__()
        self.editor = CodeEditor()
        self.editor.setPlainText(fileProxy.text)
        self.editor.file = fileProxy
        fileProxy.hasUnsavedChanges = False
        self.tabName = "{}/{}".format(fileProxy.parent.path, fileProxy.path)

class EditorTabWidget(QTabWidget):
    
    def __init__(self):
        super(EditorTabWidget, self).__init__()
        self.tabBar().setStyleSheet("background-color:#007ACC;color: white; height: 20px")
        self.tabBar().setMaximumHeight(30)
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.projectTabs = dict()
        self.tabs = []
        self.setTabsClosable(True)
        self.setMovable(False)
        self.tabCloseRequested.connect(self.closeTab)

    def addNewTab(self, fileProxy, update=True):
        key = "{}/{}".format(fileProxy.parent.path, fileProxy.path)
        if key in self.projectTabs:
            self.setCurrentIndex(self.tabs.index(fileProxy))
            return
        tab = EditorTab(fileProxy)
        self.projectTabs[key] = tab
        self.addTab(tab.editor, tab.tabName)
        if update:
            self.tabs.append(fileProxy)
        self.setCurrentIndex(self.tabs.index(fileProxy))

    def getCurrentFileProxy(self):
        return self.tabs[self.currentIndex()]

    def getCurrentTab(self):
        proxy = self.getCurrentFileProxy()
        key = "{}/{}".format(proxy.parent.path, proxy.path)
        if key in self.projectTabs:
            return self.projectTabs[key]
        return None

    def closeAllTabs(self):
        for index in range(len(self.tabs)-1, -1, -1):
            if not self.closeTab(index):
                return False
        return True

    def closeTab(self, index, askToSave=True):
        proxy: FileProxy = self.tabs[index]
        key = "{}/{}".format(proxy.parent.path, proxy.path)
        if proxy.hasUnsavedChanges and askToSave:
            msg = QMessageBox()
            msg.setStyleSheet("background-color: #2D2D30; color: white;")
            msg.setParent(None)
            msg.setModal(True)
            msg.setWindowTitle("Close tab")
            msg.setText("The file {}/{} has been modified.".format(proxy.parent.path, proxy.path))
            msg.setInformativeText("Do you want to save changes?")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Save)
            retValue = msg.exec_()
            if retValue == QMessageBox.Save:
                proxy.saveFile()
            elif retValue == QMessageBox.Discard:
                pass
            else:
                return False
        self.tabs.pop(index)
        del self.projectTabs[key]
        self.removeTab(index)
        return True