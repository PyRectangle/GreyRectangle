from pygame.locals import *
from Frame.baseFunctions import *
from Frame.Render import Render
import screeninfo
import pygame


class Window:
    def __init__(self, title = "PyGame Window", frameSize = (800, 450), surfaceSize = (1920, 1080), flags = 0,
                 autoResizing = True, fullscreen = False):
        output("Window: Initializing pygame...", "debug")
        pygame.init()
        output("Window: Setting title, start size, flags and window resolution multiplier...", "debug")
        self.__title = title
        self.__lastFlags = flags
        self.flags = flags
        self.START_FRAME_SIZE = frameSize
        self.START_SURFACE_SIZE = surfaceSize
        output("Window: Getting the Resolution of the screen...", "debug")
        self.RESOLUTION = screeninfo.get_monitors()[0]
        self.WINDOW_RES_MULTIPLIER = self.START_FRAME_SIZE[1] / self.START_FRAME_SIZE[0]
        self.size = self.START_FRAME_SIZE
        self.isOpen = True
        self.fullscreen = False
        self.__surfaceX = 0
        self.__surfaceY = 0
        self.__surfaceSize = frameSize
        self.autoResizing = autoResizing
        self.fps = 0
        self.dt = 0
        self.keys = []
        for i in range(323):
            self.keys.append(0)
        self.clock = pygame.time.Clock()
        self.__getMouseStates()
        self.surfaceSize = surfaceSize
        output("Window: Creating Render object...", "debug")
        self.render = Render(self)
        output("Window: Creating Surface object...", "debug")
        self.surface = pygame.Surface(self.surfaceSize)
        output("Window: Creating window...")
        self.screen = pygame.display.set_mode(self.START_FRAME_SIZE, self.flags)
        output("Window: Setting the caption to " + self.__title + "...", "debug")
        pygame.display.set_caption(self.__title)
        if fullscreen:
            self.toggleFullscreen()

    def getTitle(self):
        return self.__title

    def setTitle(self, title):
        self.__title = title
        output("Window: Setting title to " + self.__title + "...", "debug")
        pygame.display.set_caption(self.__title)

    def __resize(self, size, extraFlags = 0, setPos = True):
        if setPos:
            os.environ['SDL_VIDEO_WINDOW_POS'] = ""
        self.size = list(size)
        output("Window: Setting mode...", "debug")
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.size, self.flags | pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size, self.flags)
        self.__surfaceSize = self.size
        do = True
        resizeCount = 0
        output("Window: Getting aspect ratio...", "debug")
        while self.__surfaceSize[0] > self.size[0] or self.__surfaceSize[1] > self.size[1] or do:
            resizeCount += 1
            do = False
            if resizeCount > 2:
                self.__surfaceSize[0] -= 1
                self.__surfaceSize[1] -= 1
            if self.__surfaceSize[0] < self.__surfaceSize[1] or resizeCount > 1:
                self.__surfaceSize = [self.__surfaceSize[0], int(self.__surfaceSize[0] * self.WINDOW_RES_MULTIPLIER)]
            elif self.__surfaceSize[0] > self.__surfaceSize[1] or resizeCount > 1:
                self.__surfaceSize = [int(self.__surfaceSize[1] / self.WINDOW_RES_MULTIPLIER), self.__surfaceSize[1]]
        self.__surfaceX = int(self.size[0] / 2 - self.__surfaceSize[0] / 2)
        self.__surfaceY = int(self.size[1] / 2 - self.__surfaceSize[1] / 2)

    def __getMouseStates(self):
        self.mousePressed = pygame.mouse.get_pressed()
        try:
            self.mousePos = list(pygame.mouse.get_pos())
            self.mousePos[0] -= self.__surfaceX
            self.mousePos[1] -= self.__surfaceY
            for i in range(2):
                self.mousePos[i] /= self.__surfaceSize[i] / self.START_SURFACE_SIZE[i]
                self.mousePos[i] = int(self.mousePos[i])
        except ZeroDivisionError:
            pass

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.isOpen = False
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = 1
        if event.type == pygame.KEYUP:
            self.keys[event.key] = 0
        if event.type == pygame.VIDEORESIZE:
            if self.autoResizing:
                output("Window: Resizing the window from " + str(tuple(self.size)) + " to " + str(event.size) + "...",
                       "debug")
                self.__resize(event.size)
    
    def updateClock(self):
        self.clock.tick(0)
        self.fps = self.clock.get_fps()
        self.dt = self.clock.get_time()

    def update(self):
        self.updateClock()
        self.__getMouseStates()
        for event in pygame.event.get():
            self.handleEvent(event)
        if self.flags != self.__lastFlags:
            self.startDisplay()
        self.__lastFlags = self.flags

    def updateDisplay(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.surface, tuple(self.__surfaceSize)), (self.__surfaceX,
                                                                                           self.__surfaceY))
        pygame.display.update()

    def toggleFullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.__resize((self.RESOLUTION.width, self.RESOLUTION.height), True, pygame.FULLSCREEN)
        else:
            self.__resize(self.START_FRAME_SIZE, False)

    title = property(getTitle, setTitle)
