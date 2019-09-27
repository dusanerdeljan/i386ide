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

class Stack:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, elem):
        self._data.append(elem)

    def pop(self):
        if self.is_empty():
            raise Exception('Stack is empty!')

        return self._data.pop()

    def top(self):
        if self.is_empty():
            raise Exception('Stack is empty!')

        return self._data[-1]

    def clear(self):
        self._data.clear()
