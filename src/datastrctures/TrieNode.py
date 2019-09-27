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

from src.datastrctures.MyQueue import Queue


class TrieNode(object):

    # vrednost na koju se postavlja node koji oznacava kraj reci
    _NULL_TERMINATOR = -1

    def __init__(self, value=_NULL_TERMINATOR,):
        self.value = value
        self.children = dict()

    def search_word(self, char_queue: Queue):
        # ako je red prazan onda je rec pronadjena akko se _NULL_TERMINATOR nalazi u listi dece tekuceg cvora
        if char_queue.is_empty():
            if self.is_end_of_word():
                return True
            return False
        char = char_queue.dequeue()
        # ako se sledece slovo ne nalazi kao kljuc u mapi dece znaci
        # da ta rec ne postoji pa vrati False
        if char not in self.children:
            return False, None
        # ako se nalazi nastavi postupak rekurzivno
        return self.children[char].search_word(char_queue)

    def search_prefix(self, char_queue: Queue):
        # ako je red prazan znaci da prefiks postoji
        if char_queue.is_empty():
            return True
        char = char_queue.dequeue()
        # ako se sledeec slove ne nalazi kao kljuc u mapi dece tekuceg cvora znaci da taj prefiks ne postoji
        if char not in self.children:
            return False, None
        return self.children[char].search_prefix(char_queue)

    # vrati sve dostupne reci iz trenutnog cvora
    def get_words(self):
        words = []
        if self.is_leaf():
            words.append("")
            return words
        for char in self.children:
            new_words = self.children[char].get_words()
            for new_word in new_words:
                words.append(self.value + new_word)
        return words


    # key - kljuc stranice u recniku podataka
    def insert(self, char_queue: Queue):
        # ako nema vise slova postavi null terminator node
        if char_queue.is_empty():
            self.children[self._NULL_TERMINATOR] = TrieNode()
            return
        # uzmi sledece slovo iz reda
        char = char_queue.dequeue()
        # ako u mapi dece ne postoji dete sa tim slovom napravi ga
        if char not in self.children:
            self.children[char] = TrieNode(char)
        child = self.children[char]
        # rekurzivno dodaj ostatak slova iz reda
        child.insert(char_queue)

    # vraca podtrie
    def get_subtrie(self, char_queue: Queue):
        # ako nema vise slova vrati trenutni cvor
        if char_queue.is_empty():
            return self
        char = char_queue.dequeue()
        # ako se slovo ne nalazi kao kljuc u mapi dece
        if char not in self.children:
            return None
        # ako se slovo nalazi kao kljuc u mapi dece nastavi postupak rekurzivno
        return self.children[char].get_subtrie(char_queue)

    def is_end_of_word(self):
        return self._NULL_TERMINATOR in self.children

    def child_count(self):
        return len(self.children)

    def is_empty(self):
        return self.value == self._NULL_TERMINATOR

    def is_root(self):
        return self.is_empty() and self.child_count() > 0

    def is_leaf(self):
        return self.is_empty() and not self.is_root()