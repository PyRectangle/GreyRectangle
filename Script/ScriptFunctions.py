class ScriptFunctions:
    def __init__(self, main):
        self.main = main
        self.postToChat = self.main.player.chat.chatMessages.postMessage
