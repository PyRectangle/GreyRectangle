from Frame.gui.GuiHandler import GuiHandler
from Frame.KeyDict import KeyDict
from Frame.baseFunctions import *
from Frame.Render import Render
from pygameImporter import *
import screeninfo


class Window:
    def __init__(self, title = "PyGame Window", frameSize = (800, 450), surfaceSize = (1920, 1080), flags = 0,
                 autoResizing = True, fullscreen = False, icon = None):
        output("Window: Initializing pygame...", "debug")
        pygame.mixer.init(buffer=64)
        pygame.init()
        output("Window: Setting title, start size, flags and window resolution multiplier...", "debug")
        self.__title = title
        self.__lastFlags = flags
        self.flags = flags
        self.START_FRAME_SIZE = frameSize
        self.START_SURFACE_SIZE = surfaceSize
        output("Window: Getting the Resolution of the screen...", "debug")
        self.RESOLUTION = screeninfo.get_monitors()[0]
        output("Window: Getting aspect ratio...", "complete")
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
        self.fpsLimit = 0
        output("Window: Creating gui handler object...", "debug")
        self.disableGuiComeInAnimations = True
        self.disableGuiAnimations = True
        self.guiChanger = K_TAB
        self.guiPresser = K_RETURN
        self.guiEscape = K_ESCAPE
        self.guiMove = [K_LEFT, K_RIGHT]
        self.guiHandler = GuiHandler(self)
        self.useBusyLoop = True
        self.char = ""
        self.keys = KeyDict()
        self.clock = pygame.time.Clock()
        self.__getMouseStates()
        self.surfaceSize = surfaceSize
        if icon != None:
            pygame.display.set_icon(icon)
        output("Window: Creating Render object...", "debug")
        self.render = Render(self)
        output("Window: Creating Surface object...", "debug")
        self.surface = pygame.Surface(self.surfaceSize)
        output("Window: Creating window...")
        if fullscreen:
            self.sizeBeforeFullscreen = self.START_FRAME_SIZE
            self.fullscreen = True
            self.size = (self.RESOLUTION.width, self.RESOLUTION.height)
            self.__surfaceSize = [*self.__getAspectRatio(self.RESOLUTION.width, self.RESOLUTION.height)]
            self.__surfaceX = int(self.RESOLUTION.width / 2 - self.__surfaceSize[0] / 2)
            self.__surfaceY = int(self.RESOLUTION.height / 2 - self.__surfaceSize[1] / 2)
            self.screen = pygame.display.set_mode((self.RESOLUTION.width, self.RESOLUTION.height), self.flags | pygame.FULLSCREEN | pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode(self.START_FRAME_SIZE, self.flags)
        output("Window: Setting the caption to " + self.__title + "...", "debug")
        pygame.display.set_caption(self.__title)
        self.icon = icon
        self.screenSurfaces = []
        
    def getTitle(self):
        output("Window: Getting window title...", "debug")
        return self.__title

    def setTitle(self, title):
        self.__title = title
        output("Window: Setting title to " + self.__title + "...", "debug")
        pygame.display.set_caption(self.__title)
    
    def __getAspectRatio(self, width, height):
        if width * self.WINDOW_RES_MULTIPLIER < height:
            height = width * self.WINDOW_RES_MULTIPLIER
        if height / self.WINDOW_RES_MULTIPLIER < width:
            width = height / self.WINDOW_RES_MULTIPLIER
        return int(width), int(height)

    def resize(self, size, setPos = True, reset = False):
        loop = 1
        if reset:
            loop = 2
        for i in range(loop):
            if setPos:
                os.environ['SDL_VIDEO_WINDOW_POS'] = ""
            if reset:
                self.fullscreen = False
                pygame.display.quit()
                pygame.display.init()
                os.environ['SDL_VIDEO_WINDOW_POS'] = str(int(self.RESOLUTION.width / 2 - size[0] / 2)) + ", " + str(int(self.RESOLUTION.height / 2 - self.size[1] / 2))
            self.size = list(size)
            output("Window: Setting mode to " + str(tuple(self.size)) + "...", "debug")
            if self.fullscreen:
                self.screen = pygame.display.set_mode(self.size, self.flags | pygame.FULLSCREEN | pygame.NOFRAME)
            else:
                self.screen = pygame.display.set_mode(self.size, self.flags)
            self.__surfaceSize = self.size
            output("Window: Getting aspect ratio...", "debug")
            self.__surfaceSize = list(self.__getAspectRatio(self.__surfaceSize[0], self.__surfaceSize[1]))
            self.__surfaceX = int(self.size[0] / 2 - self.__surfaceSize[0] / 2)
            self.__surfaceY = int(self.size[1] / 2 - self.__surfaceSize[1] / 2)

    def __getMouseStates(self):
        output("Window: Getting mouse states...", "complete")
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
            output("Window: Quitting...")
            self.isOpen = False
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = 1
            self.char = event.unicode
        if event.type == pygame.KEYUP:
            self.keys[event.key] = 0
        if event.type == pygame.VIDEORESIZE:
            if self.autoResizing:
                output("Window: Resizing the window from " + str(tuple(self.size)) + " to " + str(event.size) + "...", "debug")
                self.resize(event.size)
        if event.type == pygame.MOUSEMOTION:
            output("Window: Got mouse movement", "complete")
            self.guiHandler.keyActive = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            output("Window: Mouse button was pressed", "debug")
            self.guiHandler.keyActive = False
            if event.button == 4:
                self.mouseScroll = -1
            if event.button == 5:
                self.mouseScroll = 1
    
    def updateClock(self):
        output("Window: Getting FPS and delta time...", "complete")
        if self.useBusyLoop:
            self.dt = self.clock.tick_busy_loop(self.fpsLimit)
        else:
            self.dt = self.clock.tick(self.fpsLimit)
        self.fps = self.clock.get_fps()

    def update(self):
        self.char = ""
        self.updateClock()
        self.mouseScroll = 0
        self.__getMouseStates()
        output("Window: Handling events...", "complete")
        for event in pygame.event.get():
            self.handleEvent(event)
        output("Window: Looking for a flag change...", "complete")
        if self.flags != self.__lastFlags:
            self.startDisplay()
        self.__lastFlags = self.flags
        output("Window: Updating gui handler...", "complete")
        self.guiHandler.update()
    
    def startDisplay(self):
        output("Window: Starting display...", "complete")
        self.screen = pygame.display.set_mode(self.size, self.flags)
    
    def getScreenCoords(self, x, y):
        x *= self.__surfaceSize[0] / self.START_SURFACE_SIZE[0]
        y *= self.__surfaceSize[1] / self.START_SURFACE_SIZE[1]
        x += self.__surfaceX
        y += self.__surfaceY
        return x, y
    
    def getScreenScale(self, scale, axis):
        scale *= self.__surfaceSize[axis] / self.START_SURFACE_SIZE[axis]
        return int(scale + 0.5)
    
    def onOptionalSurfaceRender(self):
        pass

    def updateDisplay(self):
        output("Window: Updating display...", "complete")
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.surface, tuple(self.__surfaceSize)), (self.__surfaceX, self.__surfaceY))
        for surface in self.screenSurfaces:
            self.screen.blit(surface, (0, 0))
            self.onOptionalSurfaceRender()
        pygame.display.update()

    def toggleFullscreen(self):
        output("Window: Toggling full screen...", "debug")
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.sizeBeforeFullscreen = self.size
            self.resize((self.RESOLUTION.width, self.RESOLUTION.height))
        else:
            os.environ['SDL_VIDEO_WINDOW_POS'] = str(int(self.RESOLUTION.width / 2 - self.sizeBeforeFullscreen[0] / 2)) + ", " + \
                                                 str(int(self.RESOLUTION.height / 2 - self.sizeBeforeFullscreen[1] / 2))
            self.resize(self.sizeBeforeFullscreen, False)

    title = property(getTitle, setTitle)
