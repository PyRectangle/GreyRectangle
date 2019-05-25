from Frame.baseFunctions import setColorkey
from pygameImporter import pygame
import pygame as pyg
import av


class Movie:
    def __init__(self, file, fps, main, movieNum, colorkey = None, textureFrame = 0):
        self.container = av.open(file)
        self.duration = int(self.container.duration / (4000 / 0.24) + 1)
        self.fps = fps
        self.openProgress = 0
        self.progress = main.progress
        self.time = 0
        self.play = False
        self.frames = []
        self.args = [None]
        self.p = file == "resources/images/RectangleAppear.mkv"
        self.colorkey = colorkey
        for frame in self.container.decode(video=0):
            self.frames.append(self.__getFrameAsSurface(frame))
            if main != None:
                self.openProgress = len(self.frames) / self.duration * 100
                main.setProgress(self.progress + self.openProgress / movieNum - 0.01)
        self.surface = self.frames[0]
        self.main = main
        self.textureFrame = textureFrame
        self.container.close()
    
    def update(self, dt):
        if not self.main.config.config["BlockAnimations"]:
            self.frame = 0
            self.time = 0
            self.finishedPlaying(*self.args)
            self.finishedPlaying = self.finishedPlayingBack
            self.args = [None]
            self.surface = self.frames[self.textureFrame]
        elif self.play:
            self.time += dt / 1000
            self.frame = int(self.time * self.fps)
            if self.frame >= self.duration:
                self.frame = 0
                self.time = 0
                self.finishedPlaying(*self.args)
                self.finishedPlaying = self.finishedPlayingBack
                self.args = [None]
            self.surface = self.frames[self.frame]
        
    def finishedPlaying(self, *args):
        pass

    def finishedPlayingBack(self, *args):
        pass

    def __getFrameAsSurface(self, frame):
        image = frame.to_image()
        mode = image.mode
        size = image.size
        data = image.tobytes()
        if pygame.K_F11 > 1000:
            osurface = pyg.image.fromstring(data, size, mode)
            surface = pygame.Surface(size).convert()
            for y in range(list(size)[1]):
                for x in range(list(size)[0]):
                    surface.set_at((x, y), pygame.Color(osurface.get_at((x, y))))
        else:
            surface = pygame.image.fromstring(data, size, mode).convert()
            if self.colorkey != None:
                return setColorkey(self.colorkey, surface)
        return surface
