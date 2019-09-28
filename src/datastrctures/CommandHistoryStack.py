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

class CommandHistoryStack(object):

    def __init__(self):
        self.history = []
        self.currentIndex = 0
        self.limit = 5

    def push(self, command):
        if len(self.history) > 0:
            if command == self.history[-1]:
                return
        self.history.append(command)
        if len(self.history) > self.limit:
            self.history.pop(0)
        self.currentIndex = len(self.history)

    def __iter__(self):
        for i in range(len(self.history), -1, -1):
            yield self.history[i]

    def getPrev(self):
        if len(self.history) == 0:
            return ""
        temp = self.currentIndex
        temp -= 1
        if temp >= 0:
            self.currentIndex = temp
        return self.history[self.currentIndex]

    def getNext(self):
        if self.currentIndex == len(self.history):
            return ""
        temp = self.currentIndex
        temp += 1
        if temp <= len(self.history) - 1:
            self.currentIndex = temp
        else:
            return ""
        return self.history[self.currentIndex]