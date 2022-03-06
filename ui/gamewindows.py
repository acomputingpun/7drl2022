from . import warps, windows
#from . import warps, windows, gridpanels, syspanels, nonpanels, attpanels, messages, backpanels, animas
#from . import fx
#import random

class GameWindow(windows.Window):
    def __init__(self, interf):
        super().__init__(interf)

        self.gridPanel = GridPanel(self)
#        self.backPanel = backpanels.BackgroundPanel(self)
        self.msgPanel = MessagePanel(self)

        self.children = [self.gridPanel, self.msgPanel]

    def requestActionWarp(self):
        raise NotImplementedError()

    @property
    def hero(self):
        return self.interf.state.hero

    def drawContents(self, ren):
        ren.drawText( (0,0), "hello world" )

class GameWindowWarp(warps.Warp):
    def warpArrowKey(self, key, shift = False):
        pass

    def warpOtherKey(self, key):
        if key == 113: # q
            pass
        elif key == 119: # w
            pass
        elif key == 101: # e
            pass
        elif key == 114: # r
            pass
        elif key == 97: # a
            pass
        elif key == 115: #s
            pass
        elif key == 100: #d
            pass
        elif key == 9: # tab
            pass
        else:
            print ("Key was", key)

from . import scions
import vecs, utils

class MessagePanel(scions.Panel):
    xyAnchor = (0, 44)

    def drawContents(self, ren):
        ren.drawText( (0, 0), "messagepanel")

    @property
    def panelSize(self):
        return vecs.Vec2(60, 6)

class GridPanel(scions.Panel):
    TILE_SPACING = 4
    TILES_ON_GRID = 11
    xyAnchor = (1, 1)

    def __init__(self, parent):
        super().__init__(parent)

        self.trMatrix = [[TileReflection(self, vecs.Vec2(x,y)) for y in range(self.TILES_ON_GRID)] for x in range(self.TILES_ON_GRID)]

        self.children = [k for k in self.allTiles()]

    @property
    def xyTileSize(self):
        return vecs.Vec2(self.TILES_ON_GRID, self.TILES_ON_GRID)
    def allPoses(self):
        return utils.allPoses((0,0), self.xyTileSize)
    def allTiles(self):
        for pos in self.allPoses():
            yield self.lookup(pos)
    def lookup(self, xyPos):
        if self.rectContains(xyPos):
            return self.trMatrix[xyPos[0]][xyPos[1]]
        else:
            return None
    def rectContains(self, xyPos):
        return utils.rectContains(((0,0), self.xyTileSize), xyPos)


    @property
    def panelSize(self):
        return vecs.Vec2(43, 43)

    def drawContents(self, ren):
        ren.drawText( (0, 0), "gridpanel")

    def xyTileToNW(self, xyTile):
        return (xyTile * self.TILE_SPACING)
    def xyTileToCenter(self, xyTile):
        return self.xyTileToNW(xyTile) + (1, 1)

class TileReflection(scions.Panel):
    def __init__(self, parent, xyTile):
        super().__init__(parent)
        self.xyTile = xyTile
        self.xyAnchor = self.parent.xyTileToNW(xyTile)

    @property
    def panelSize(self):
        return vecs.Vec2(3, 3)

    def drawContents(self, ren):
        pass
#    def draw(self):
#        pass
