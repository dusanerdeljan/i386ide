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