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

class QueueError(Exception):
    pass


class Queue(object):
    def __init__(self, capacity=2):
        self._data = [None] * capacity
        self._f = 0
        self._size = 0

    def __len__(self):
        return self._size
    
    def __str__(self):
        if self.is_empty():
            return "Queue is empty."
        result = ""
        for i in range(self._size):
            result += str(self._data[(self._f + i) % len(self._data)]) + " "
        return result

    def __iter__(self):
        for i in range(self._size):
            yield self._data[(self._f + i) % len(self._data)]
    
    def is_empty(self):
        return self._size == 0

    # prilikom izbacivanja elementa sa vrha reda ukoliko broj elemenata niza padne ispod 1/4 kapaciteta potrebno je prepoloviti kapacitet
    # prilikom stavljanja nogog elementa u red ukoliko broj elemenata poraste preko 1/2 kapaciteta potrebno je duplirati kapacitet
    def _resize(self, capacity):
        old = self._data
        self._data = [None] * capacity
        first = self._f
        for i in range(self._size):
            self._data[i] = old[first]
            first = (first+1) % len(old)
        self._f = 0

    def first(self):
        if self.is_empty():
            raise QueueError("Queue is empty!")
        return self._data[self._f]

    def dequeue(self):
        if self.is_empty():
            raise QueueError("Queue is empty!")
        value = self._data[self._f]
        self._f = (self._f + 1) % len(self._data)
        self._size -= 1
        # ako broj elemenata padne ispod 1/4 kapaciteta niza treba prepolivoti kapacitet
        if self._size < 0.25 * len(self._data):
            self._resize(len(self._data)//2)
        return value

    def enqueue(self, elem):
        # if self._size == len(self._data):
        #     self._resize(2*len(self._data))
        index = (self._f + self._size) % len(self._data)
        self._data[index] = elem
        self._size += 1
        # ako broj elemenata predje 1/2 kapaciteta niza treba dupliarati kapacitet
        if self._size > 0.5 * len(self._data):
            self._resize(2*len(self._data))

    

    