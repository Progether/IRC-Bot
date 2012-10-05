class ChatLog:

    def __init__(self):
        self.LOG_LENGTH = 15
        self.chats = list()
    
    def addLog(self, logMessage):
        self.chats.append(logMessage)
        if len(self.chats) >= self.LOG_LENGTH:
            del self.chats[0]
    
    def playLog(self):
        for msg in self.chats:
            print msg