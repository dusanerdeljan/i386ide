from src.datastrctures.TrieNode import TrieNode
from src.datastrctures.MyQueue import Queue

class Trie(object):
    """
    Klasa modeluje Trie strukturu podataka
    Attributes:
        root (TrieNode): Korenski cvor
    """

    def __init__(self):
        """
        Konstruktor
        Inicijalizuj korenski cvor na prazan cvor
        """
        self.root = TrieNode()

    def _get_char_queue(self, chars):
        """
        Metoda vraca red ciji su elementi karakteri u prosledjenom stringu
        :param chars (str): Rec koja treba da se pretvori u red
        :return: Queue Red karaktera
        """
        char_queue = Queue()
        for i in range(len(chars)):
            char_queue.enqueue(chars[i])
        return char_queue

    def get_autocompletes(self, word: str):
        # ako postoji se trazena rec nalazi u stablu kao prefiks nadji sve reci ciji je to prefiks
        # ako nije prefiks probaj da odseces poslednji karakter pa ponovi postupak sve dok ne dodjes do praznog stirnga
        while word != "":
            is_prefix = self.search_prefix(word)
            if is_prefix:
                node = self.get_subtrie(word)
                found_words = node.get_words()
                for i in range(len(found_words)):
                    end = found_words[i]
                    found_words[i] = word[:-1] + end
                return found_words
            word = word[:-1]
        return None

    def search(self, word: str):
        char_queue = self._get_char_queue(word)
        return self.root.search_word(char_queue)

    def search_prefix(self, prefix: str):
        char_queue = self._get_char_queue(prefix)
        return self.root.search_prefix(char_queue)

    def get_words(self, word: str):
        node = self.get_subtrie(word)
        words = node.get_words()
        # odseci poslednje slovo u reci da se ne bi dupliralo
        begin = word[:-1]
        for i in range(len(words)):
            end = words[i]
            words[i] = begin + end
        return words

    def insert(self, word):
        char_queue = self._get_char_queue(word)
        self.root.insert(char_queue)

    def get_subtrie(self, word: str):
        char_queue = self._get_char_queue(word)
        node = self.root.get_subtrie(char_queue)
        return node