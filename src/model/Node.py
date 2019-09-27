"""
    This file is part of i386ide.
    i386ide is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PySide2.QtWidgets import QTreeWidgetItem, QMenu
from src.controller.PathManager import PathManager

class Node(QTreeWidgetItem):

    def __init__(self):
        super(Node, self).__init__()
        self.path = None

    def getContextMenu(self) -> QMenu:
        return QMenu()