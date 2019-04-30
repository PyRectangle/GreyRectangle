from Frame.gui.LineEdit import LineEdit
from Frame.gui.Button import Button
from Constants import *
from Menu import Menu


class ChatMenu(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.addGui(LineEdit, ((100, 100, 100), (255, 100, 100), CHAT_MESSAGE_MAX_CHARS, 10, 1010, 1420, 60, "", (100, 100, 100), (110, 110, 110), (90, 90, 90),
                               (0, 0, 0), FONT, True, 10, 10, 0.2, True, [0, -1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.main.player.chat.chatMessages.clearChat, (), 10, 10, 400, 100, "Clear", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0),
                             FONT, True, 30, 30, 0.1, True, [0, 1], None, SOUNDS, menuHandler.window))
