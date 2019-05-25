from Script.Player import Player
from Constants import *


class ScriptFunctions:
    def __init__(self, main):
        self._main = main
        self.postToChat = self._main.player.chat.chatMessages.postMessage
        self.player = Player(main)
