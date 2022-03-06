import time
import sdl2, sdl2.ext, ctypes
import os
import utils

class EventHandler():
    def warpEvents(self, warp):
        event = sdl2.SDL_Event()
        if sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                warp.warpQuit()
            elif event.type == sdl2.SDL_KEYDOWN:
                warp.warpKeydown(event.key.keysym.sym)

#GLYPH_X, GLYPH_Y = (10, 10)
GLYPH_X, GLYPH_Y = (16, 16)

class Renderer():
    def __init__(self, xSize, ySize):
        sdl2.ext.init()
        self.window = sdl2.SDL_CreateWindow(b"7DRL 2022!",
                                            sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
                                            1200, 800, sdl2.SDL_WINDOW_SHOWN)
        self.rcon = sdl2.SDL_CreateRenderer(self.window, -1, 0)
#        self.con = sdl2.SDL_GetWindowSurface(self.window)

        self.xSize, self.ySize = xSize, ySize
        self.zBuffer = [[0 for y in range(ySize)] for x in range(xSize)]
        self.matrix = [[32 for y in range(ySize)] for x in range(xSize)]
        self.fgMatrix = [[(255, 255, 255) for y in range(ySize)] for x in range(xSize)]
        self.bgMatrix = [[(0, 0, 0) for y in range(ySize)] for x in range(xSize)]
        self.dirty = [[True for y in range(ySize)] for x in range(xSize)]

        self.xyOffset = (0,0)
        self.zLevel = 0

        self.setup()

    def setup(self):
#        print ("Valid image formats:", sdl2.ext.get_image_formats())
        baseSheet = sdl2.ext.load_image(os.path.join(os.path.dirname(os.path.realpath(__file__)), "sbascii16x16.bmp"))
        sdl2.SDL_SetColorKey(baseSheet, True, 0)
        self.baseTex = sdl2.SDL_CreateTextureFromSurface(self.rcon, baseSheet)

#        self.nameMap = [
#        ' !"#$%&\'()*+,-./0123456789:;<=>?',
#        '@[\\]^_`{|}~',
#        '',
#        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
#        'abcdefghijklmnopqrstuvwxyz'
#        ]
#        NAME_MAP_Y = 8
#        NAME_MAP_X = 32


        self.nameMap = [
        '',
        '',
        ' !"#$%&\'()*+,-./',
        '0123456789:;<=>?',
        '@ABCDEFGHIJKLMNO',
        'PQRSTUVWXYZ[\\]^_',
        '`abcdefghijklmno',
        'pqrstuvwxyz{|}~',
        ]
        NAME_MAP_Y = 16
        NAME_MAP_X = 16

        self.charMap = {}
        self.intMap = []

        tempSurface = sdl2.SDL_CreateRGBSurface(0, GLYPH_X, GLYPH_Y, 32, 0, 0, 0, 0)

        for y in range(NAME_MAP_Y):
            for x in range(NAME_MAP_X):
                try:
                    self.intMap.append(sdl2.SDL_Rect(x*GLYPH_X, y*GLYPH_Y, GLYPH_X, GLYPH_Y))
                    tileName = self.nameMap[y][x]
                    charCode = ord(tileName)
                    self.charMap[charCode] = sdl2.SDL_Rect(x*GLYPH_X, y*GLYPH_Y, GLYPH_X, GLYPH_Y)
#                    self.charMap[charCode] = sdl2.SDL_CreateTextureFromSurface(self.rcon, tempSurface)
                except IndexError:
                    pass


    def drawChar(self, xyPos, char, fg=None, bg=None):
        self.put(xyPos[0]+self.xyOffset[0], xyPos[1]+self.xyOffset[1], self.zLevel, ord(char), fg, bg)
    def drawXChar(self, xyPos, value = None, fg=None, bg=None):
        self.put(xyPos[0]+self.xyOffset[0], xyPos[1]+self.xyOffset[1], self.zLevel, value, fg, bg)        

    def drawAlpha(self, xyPos, fg=None, bg=None, opacity = 1):
        x, y = (xyPos[0]+self.xyOffset[0], xyPos[1]+self.xyOffset[1])
        if 0<=x<self.xSize and 0<=y<self.ySize:
            if bg != None:
                bg = utils.interp3( self.bgMatrix[x][y], opacity, bg )
            if fg != None:
                fg = utils.interp3( self.fgMatrix[x][y], opacity, bg )
            self.put(x, y, self.zLevel, fg=fg, bg=bg)

    def drawText(self, xyPos, text, fg=None, bg=None):
        xLoc, yLoc = xyPos
        for char in text:
            self.put(xLoc+self.xyOffset[0], yLoc+self.xyOffset[1], self.zLevel, ord(char), fg, bg)
            xLoc += 1

    def put(self, x,y,z, value = None, fg=(255,255,255), bg=(0,0,0)):
        if 0<=x<self.xSize and 0<=y<self.ySize:
            if self.zBuffer[x][y] <= z:
                self.zBuffer[x][y] = z
                if value != None:
                    if self.matrix[x][y] != value:
                        self.matrix[x][y] = value
                        self.dirty[x][y] = True
                if fg != None:
                    if self.fgMatrix[x][y] != fg:
                        self.fgMatrix[x][y] = fg
                        self.dirty[x][y] = True
                if bg != None:
                    if self.bgMatrix[x][y] != bg:
                        self.bgMatrix[x][y] = bg
                        self.dirty[x][y] = True

    def flush(self):
        for y in range(self.ySize):
            for x in range(self.xSize):
                if self.dirty[x][y]:
                    self.dirty[x][y] = False
                    if self.matrix[x][y] < 0:
                        sourceRect = self.intMap[-self.matrix[x][y]]
                    else:
                        sourceRect = self.charMap[self.matrix[x][y]]

                    destRect = sdl2.SDL_Rect(x*GLYPH_X,y*GLYPH_Y, GLYPH_X, GLYPH_Y)
                    sdl2.SDL_SetTextureColorMod(self.baseTex,  *self.bgMatrix[x][y])
                    sdl2.SDL_RenderCopy(self.rcon, self.baseTex, self.intMap[219], destRect)
                    sdl2.SDL_SetTextureColorMod(self.baseTex,  *self.fgMatrix[x][y])
                    sdl2.SDL_RenderCopy(self.rcon, self.baseTex, sourceRect, destRect)
#                    sdl2.SDL_BlitSurface(self.charMap[self.matrix[x][y]], None, self.con, sdl2.SDL_Rect(x*GLYPH_X,y*GLYPH_Y, GLYPH_X, GLYPH_Y))
#        sdl2.SDL_UpdateWindowSurface(self.window)
        sdl2.SDL_RenderPresent(self.rcon);
        self.zBuffer = [[0 for y in range(self.ySize)] for x in range(self.xSize)]
        self.zLevel = 0

    def forceQuit(self):
        exit()

def systemMS():
    return time.time() * 1000
class SystemTimer():
    def __init__(self):
        self._initMS = systemMS()
    def MS(self):
        return systemMS() - self._initMS
