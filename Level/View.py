from Editor.Actions import Actions
from pygameImporter import pygame
from Constants import *


class View:
    def __init__(self, main):
        self.window = main.window
        self.main = main
        self.showLevel = None
        self.level = None
        self.size = VIEW_MIN_SIZE
        self.moveSize = False
        self.sizeDirect = True
        self.toNormal = False
        self.opened = False
        self.canChange = True
        self.shouldRender = False
        self.canOpen = False
        self.willOpen = False
        self.useBlockWidth = False
        self.animate = self.main.config.config["LevelTransitions"]
    
    def pressLevel(self, level):
        self.showLevel = level
        self.moveSize = True
        self.sizeDirect = False
        self.shouldRender = True
        self.canOpen = False
        for block in self.main.blocks.blocks:
            try:
                for resource in block.overlayResources:
                    if type(resource) != pygame.Surface:
                        resource.finishedPlaying(*resource.args)
            except AttributeError:
                pass
            if block.lastBlockObject != None:
                block.lastBlockObject.setOverlay(None)
            block.lastBlockObject = None
            block.lastTouched = None
            block.overlay = {}
        if level != None:
            self.main.levelSelection.setText(level.data.description)
        
    def closeLevelSelection(self):
        if not self.main.levelSelection.toggleClosed:
            self.main.levelSelection.toggle()
        self.main.menuHandler.remove()

    def open(self):
        if self.level != None:
            self.main.levelSelection.levelGuiHandler.canChange = False
            if self.canOpen:
                self.main.levelSelection.levelGuiHandler.lastSelected = None
                self.willOpen = False
                self.opened = True
                self.toNormal = True
                self.sizeDirect = False
                self.moveSize = True
                self.closeLevelSelection()
                if self.main.menuHandler.editor:
                    self.main.editing = True
                    self.main.editor.actions = Actions(self.level, self.main)
                    self.main.editor.activeCount = 0
                    self.main.editor.active = False
                else:
                    self.main.playing = True
                    self.main.player.first = True
                    self.main.player.active = False
                    self.main.player.activeCount = 0
                self.main.camera.setProps(self.level)
            else:
                self.closeLevelSelection()
                self.willOpen = True
 
    def update(self):
        self.animate = self.main.config.config["LevelTransitions"]
        if self.moveSize:
            if self.sizeDirect:
                if not self.animate:
                    self.size = VIEW_MAX_SIZE
                self.size += self.window.dt * VIEW_SPEED
                if self.size > VIEW_MAX_SIZE:
                    self.moveSize = False
                    self.canOpen = True
                    self.size = VIEW_MAX_SIZE
            else:
                if not self.animate:
                    if self.toNormal:
                        self.size = BLOCK_SIZE
                    else:
                        self.size = VIEW_MIN_SIZE
                self.size -= self.window.dt * VIEW_SPEED
                if self.size < VIEW_MIN_SIZE:
                    self.size = VIEW_MIN_SIZE
                    self.useBlockWidth = False
                    self.main.camera.size = BLOCK_SIZE
                if self.toNormal and self.size < BLOCK_SIZE:
                    self.size = BLOCK_SIZE
                    self.toNormal = False
                    self.moveSize = False
                    self.shouldRender = False
        if self.willOpen:
            self.open()
        self.canChange = self.size == VIEW_MIN_SIZE
        if self.canChange:
            self.main.camera.setCoords(self.showLevel)
            self.level = self.showLevel
            self.sizeDirect = True
        for block in self.main.blocks.blocks:
            if block.animation:
                block.movie.update(self.main.window.dt)
                block.tmpSurface = None
            if block.overlays != None:
                for overlay in block.overlayResources:
                    if type(overlay) != pygame.Surface:
                        overlay.update(self.main.window.dt)

    
    def render(self):
        if self.level != None:
            self.main.camera.setStops(self.level, True)
            if self.main.menuHandler.goToPlay:
                renderX = self.main.camera.stop(self.main.camera.stopRight, self.main.camera.stop(self.main.camera.stopLeft, self.main.player.x, False), True)
                renderY = self.main.camera.stop(self.main.camera.stopDown, self.main.camera.stop(self.main.camera.stopUp, self.main.player.y, False), True)
            else:
                renderX = self.main.camera.stop(self.main.camera.stopRight, self.main.camera.stop(self.main.camera.stopLeft, self.level.data.spawnX, False), True)
                renderY = self.main.camera.stop(self.main.camera.stopDown, self.main.camera.stop(self.main.camera.stopUp, self.level.data.spawnY, False), True)
            if self.main.menuHandler.editor:
                renderX = self.level.data.spawnX
                renderY = self.level.data.spawnY
                if self.main.menuHandler.goToEdit:
                    renderX = self.main.editor.x
                    renderY = self.main.editor.y
            if self.opened:
                self.level.render.blocks(renderX, renderY, self.size)
                if self.main.menuHandler.editor:
                    self.level.render.grid(renderX, renderY, self.size)
            elif self.useBlockWidth:
                self.level.render.blocks(renderX, renderY, self.size, self.main.camera.size)
                if self.main.menuHandler.editor:
                    self.level.render.grid(renderX, renderY, self.main.camera.size, self.size)
            else:
                self.level.render.blocks(renderX, renderY, self.size, VIEW_DISTANCE)
                if self.main.menuHandler.editor:
                    self.level.render.grid(renderX, renderY, VIEW_DISTANCE, self.size)
        if not self.main.editing:
            self.main.player.update(False)
            self.main.player.render()
