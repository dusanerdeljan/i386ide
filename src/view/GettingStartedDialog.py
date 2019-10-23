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

from PySide2.QtWidgets import QDialog, QTextEdit, QTreeWidget, QHBoxLayout, QTreeWidgetItem
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from src.util.Documentation import Documentation
import main

class GroupNode(QTreeWidgetItem):
    
    def __init__(self, label):
        super(GroupNode, self).__init__()
        self.setText(0, label)
        self.setIcon(0, QIcon(main.resource_path("resources/help_group.png")))
        
class DocumentationNode(QTreeWidgetItem):
    
    def __init__(self, label):
        super(DocumentationNode, self).__init__()
        self.setText(0, label)
        self.setIcon(0, QIcon(main.resource_path("resources/help_doc.png")))

class DocumentationTreeView(QTreeWidget):

    def __init__(self, textEdit):
        super(DocumentationTreeView, self).__init__()
        self.textEdit = textEdit

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if not item:
            return
        super(DocumentationTreeView, self).mousePressEvent(event)
        if isinstance(item, DocumentationNode):
            self.textEdit.setHtml(Documentation.INFO[item.text(0)])

class GettingStartedDialog(QDialog):

    def __init__(self):
        super(GettingStartedDialog, self).__init__()
        self.setStyleSheet("background-color: #232323; color: white;")
        self.setWindowIcon(QIcon(main.resource_path("resources/app_icon.ico")))
        self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
        self.setWindowTitle("Help")
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml("<center><h1>i386ide\nDocumentation</h1></center>")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.treeView = DocumentationTreeView(self.textEdit)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.treeView, 1)
        self.hbox.addWidget(self.textEdit, 2)
        self.setLayout(self.hbox)
        self.treeView.setColumnCount(1)
        self.treeView.setHeaderHidden(True)
        self.treeView.setRootIsDecorated(False)
        self.setupTreeView()

    def setupTreeView(self):
        self.setupNode = GroupNode("Setup")
        self.overviewNode = DocumentationNode("Overview")
        self.linuxNode = DocumentationNode("Linux")
        self.setupNode.addChild(self.overviewNode)
        self.setupNode.addChild(self.linuxNode)
        self.getStartedNode = GroupNode("Get started")
        self.tipsNode = DocumentationNode("Tips")
        self.uiNode = DocumentationNode("User interface")
        self.settingsNode = DocumentationNode("Settings")
        self.getStartedNode.addChild(self.tipsNode)
        self.getStartedNode.addChild(self.uiNode)
        self.getStartedNode.addChild(self.settingsNode)
        self.userGuideNode = GroupNode("User guide")
        self.basicEditingNode = DocumentationNode("Basic editing")
        self.codeCompletionNode = DocumentationNode("Code completion")
        self.codeNavigationNode = DocumentationNode("Code navigation")
        self.compilingCodeNode = DocumentationNode("Compiling code")
        self.debuggingCodeNode = DocumentationNode("Debugging code")
        self.runningCodeNode = DocumentationNode("Running code")
        self.integratedTerminalNode = DocumentationNode("Integrated terminal")
        self.snippetsNode = DocumentationNode("Snippets")
        self.userGuideNode.addChild(self.basicEditingNode)
        self.userGuideNode.addChild(self.codeCompletionNode)
        self.userGuideNode.addChild(self.codeNavigationNode)
        self.userGuideNode.addChild(self.compilingCodeNode)
        self.userGuideNode.addChild(self.debuggingCodeNode)
        self.userGuideNode.addChild(self.runningCodeNode)
        self.userGuideNode.addChild(self.integratedTerminalNode)
        self.userGuideNode.addChild(self.snippetsNode)
        self.treeView.addTopLevelItem(self.setupNode)
        self.treeView.addTopLevelItem(self.getStartedNode)
        self.treeView.addTopLevelItem(self.userGuideNode)
        self.setupNode.setExpanded(True)
        self.getStartedNode.setExpanded(True)
        self.userGuideNode.setExpanded(True)

    def closeEvent(self, arg__1):
        self.hide()