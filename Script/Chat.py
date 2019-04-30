from Script.ScriptFunctions import ScriptFunctions
from Script.ChatMessages import ChatMessages
from Script.run import execute


class Chat:
    def __init__(self, main):
        self.main = main
        self.waitForInput = False
        self.write = False
        self.opened = False
        self.chatMessages = ChatMessages()
        self.scriptFunctions = None
    
    def process(self, text):
        if text[0] == "/":
            try:
                execute(text[1:], self.scriptFunctions)
            except Exception as error:
                self.chatMessages.postMessage(str(error))
        else:
            self.chatMessages.postMessage(text)
    
    def open(self):
        self.opened = True
        self.main.menuHandler.show(16)
        self.main.player.quitMenu = True
        self.write = False
        self.waitForInput = True
    
    def close(self):
        self.waitForInput = False
        self.main.menuHandler.remove()
        self.write = False
        self.main.player.quitMenu = False
        self.opened = False

    def update(self):
        if self.scriptFunctions == None:
            self.scriptFunctions = ScriptFunctions(self.main)
        self.chatMessages.update(self.main.window.dt, self.opened, self.main)
        if self.waitForInput:
            if self.main.menuHandler.chatMenu.createdGuis[0].writable:
                self.write = True
            elif self.write:
                self.waitForInput = False
                self.process(self.main.menuHandler.chatMenu.createdGuis[0].text)
                self.close()

    def render(self):
        self.chatMessages.render(self.main.window.render, self.opened)
