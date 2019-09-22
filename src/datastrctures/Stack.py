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
