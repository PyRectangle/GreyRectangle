class Block:
    def __init__(self, pos, main):
        self.data = main.player.getBlockAt(*pos, True)
        self.blockType = main.blocks.blocks[self.data[0]]
        self.pos = list(pos)
        self.setOverlay(self.blockType.startOverlay)
    
    def setOverlay(self, overlay, endFunction = None, args = None):
        self.overlay = overlay
        if self.overlay != None:
            if self.blockType.overlays[self.overlay].endswith("mkv"):
                self.blockType.overlayResources[self.overlay].frame = 0
                self.blockType.overlayResources[self.overlay].time = 0
                if self.overlay != 0:
                    self.blockType.overlayResources[self.overlay].finishedPlaying(*self.blockType.overlayResources[self.overlay].args)
                self.blockType.overlayResources[self.overlay].finishedPlaying = endFunction
                self.blockType.overlayResources[self.overlay].args = args
                self.blockType.overlayResources[self.overlay].play = True
        if self.overlay == None:
            try:
                del self.blockType.overlay[str(self.pos)]
            except KeyError:
                pass
        else:
            self.blockType.overlay[str(self.pos)] = self.overlay
