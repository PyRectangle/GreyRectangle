from Frame.gui.LineEdit import LineEdit
from Frame.gui.Button import Button
from Frame.Render import Render
from Constants import *
from Menu import Menu


class LevelOptions(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.alpha = 0
        self.up = True
        self.do = False
        self.main = menuHandler.main
        self.window = menuHandler.window
        self.renderObj = Render(menuHandler.window)
        self.texts = ["Lifes:", "Jump time:", "Jump height:", "Walk speed:", "Fall speed:", "Fall speed multiplier:", "Climb Speed:", "Description:"]
        self.startLineEditX = 850
        self.lineEditWidth = 580
        self.addGui(LineEdit, ((100, 100, 255), (200, 200, 255), 100, self.startLineEditX, 10, self.lineEditWidth, 100, "", (150, 150, 150), (0, 0, 0), (100, 100, 255),
                               (0, 0, 0), FONT, True, 30, 30, 0.1, True, [-1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(LineEdit, ((100, 100, 255), (200, 200, 255), 100, self.startLineEditX, 120, self.lineEditWidth, 100, "", (150, 150, 150), (0, 0, 0), (100, 100, 255),
                               (0, 0, 0), FONT, True, 30, 30, 0.1, True, [-1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(LineEdit, ((100, 100, 255), (200, 200, 255), 100, self.startLineEditX, 230, self.lineEditWidth, 100, "", (150, 150, 150), (0, 0, 0), (100, 100, 255),
                               (0, 0, 0), FONT, True, 30, 30, 0.1, True, [-1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(LineEdit, ((100, 100, 255), (200, 200, 255), 100, self.startLineEditX, 340, self.lineEditWidth, 100, "", (150, 150, 150), (0, 0, 0), (100, 100, 255),
                               (0, 0, 0), FONT, True, 30, 30, 0.1, True, [-1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(LineEdit, ((100, 100, 255), (200, 200, 255), 100, self.startLineEditX, 450, self.lineEditWidth, 100, "", (150, 150, 150), (0, 0, 0), (100, 100, 255),
                               (0, 0, 0), FONT, True, 30, 30, 0.1, True, [-1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(LineEdit, ((100, 100, 255), (200, 200, 255), 100, self.startLineEditX, 560, self.lineEditWidth, 100, "", (150, 150, 150), (0, 0, 0), (100, 100, 255),
                               (0, 0, 0), FONT, True, 30, 30, 0.1, True, [-1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(LineEdit, ((100, 100, 255), (200, 200, 255), 100, self.startLineEditX, 670, self.lineEditWidth, 100, "", (150, 150, 150), (0, 0, 0), (100, 100, 255),
                               (0, 0, 0), FONT, True, 30, 30, 0.1, True, [-1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(LineEdit, ((100, 100, 255), (200, 200, 255), 40, self.startLineEditX, 780, self.lineEditWidth, 100, "", (150, 150, 150), (0, 0, 0), (100, 100, 255),
                               (0, 0, 0), FONT, True, 30, 30, 0.1, True, [-1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.showEditQuit, (), 10, 990, 200, 80, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30, 0.1, True,
                             [1, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.showEditQuitSave, (), 1230, 990, 200, 80, "Ok", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30, 0.1,
                             True, [-1, -1], (60, 1240), SOUNDS, menuHandler.window))

    def update(self):
        super().update()
        if self.do:
            if self.up:
                self.alpha += self.window.dt
                if self.alpha > 255:
                    self.alpha = 255
                    self.do = False
            else:
                self.alpha -= self.window.dt
                if self.alpha < 1:
                    self.do = False
                    self.alpha = 1
    
    def renderText(self, index, size, textSize):
        text = self.texts[index]
        self.renderObj.text(FONT, textSize, text, True, (0, 0, 0), None, self.window.surface, x = 10,
                            y = index * size, alpha = self.alpha)

    def changeType(self, var, toType, name):
        try:
            realVar = toType(var)
        except:
            self.main.warningHandler.createWarning("Invalid " + name + " !", 5)
            return None
        if name != "description" and realVar <= 0:
            self.main.warningHandler.createWarning("The " + name + " must be higher than 0 !", 5)
            return None
        return realVar

    def setOptions(self):
        lifes = self.changeType(self.createdGuis[0].text, int, "lifes")
        jumpTime = self.changeType(self.createdGuis[1].text, float, "jump time")
        jumpHeight = self.changeType(self.createdGuis[2].text, float, "jump height")
        walkSpeed = self.changeType(self.createdGuis[3].text, float, "walk speed")
        fallSpeed = self.changeType(self.createdGuis[4].text, float, "fall speed")
        fallSpeedMultiplier = self.changeType(self.createdGuis[5].text, float, "fall speed multiplier")
        climbSpeed = self.changeType(self.createdGuis[6].text, float, "climb speed")
        description = self.changeType(self.createdGuis[7].text, str, "description")
        if jumpTime == None or jumpHeight == None or walkSpeed == None or fallSpeed == None or fallSpeedMultiplier == None or description == None or lifes == None or \
            climbSpeed == None:
            return False
        self.main.editor.actions.level.data.jsonData["Lifes"] = lifes
        self.main.editor.actions.level.data.jsonData["JumpTime"] = jumpTime
        self.main.editor.actions.level.data.jsonData["JumpHeight"] = jumpHeight
        self.main.editor.actions.level.data.jsonData["WalkSpeed"] = walkSpeed
        self.main.editor.actions.level.data.jsonData["FallSpeed"] = fallSpeed
        self.main.editor.actions.level.data.jsonData["FallSpeedMultiplier"] = fallSpeedMultiplier
        self.main.editor.actions.level.data.jsonData["ClimbSpeed"] = climbSpeed
        self.main.editor.actions.level.data.jsonData["Description"] = description
        self.main.editor.actions.level.data.loadJsonData()
        self.main.editor.changed = True
        self.main.levelSelection.levelGuiHandler.updateText()
        return True
    
    def create(self):
        super().create()
        self.createdGuis[0].text = str(self.main.editor.actions.level.data.jsonData["Lifes"])
        self.createdGuis[1].text = str(self.main.editor.actions.level.data.jsonData["JumpTime"])
        self.createdGuis[2].text = str(self.main.editor.actions.level.data.jsonData["JumpHeight"])
        self.createdGuis[3].text = str(self.main.editor.actions.level.data.jsonData["WalkSpeed"])
        self.createdGuis[4].text = str(self.main.editor.actions.level.data.jsonData["FallSpeed"])
        self.createdGuis[5].text = str(self.main.editor.actions.level.data.jsonData["FallSpeedMultiplier"])
        self.createdGuis[6].text = str(self.main.editor.actions.level.data.jsonData["ClimbSpeed"])
        self.createdGuis[7].text = str(self.main.editor.actions.level.data.jsonData["Description"])

    def render(self):
        super().render()
        longest = 0
        longestText = ""
        for text in self.texts:
            if len(text) > longest:
                longest = len(text)
                longestText = text
        size = self.renderObj.getTextSizeForWidth(longestText, 100, 840, FONT)
        for i in range(len(self.texts)):
            self.renderText(i, 110, size)
