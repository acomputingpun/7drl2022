from . import warps, windows
import vecs, dirconst
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

class AdvanceTimeWarp(warps.Warp):
    def warpArrowKey(self, vec, shift = False):
        print ("atw - arrow key was", vec)

    def warpOtherKey(self, key):
        print ("atw - key was", key)

    def wtransferAdvanceTime(self):
        pass
    def wtransferPlayerInput(self):
        self.transfer(GameWindowWarp(self.interf))

import actions
class GameWindowWarp(warps.Warp):
    @property
    def hero(self):
        return self.interf.state.hero

    def warpArrowKey(self, vec, shift = False):
        if vec == dirconst.IN_PLACE:
            self.trySubmitAction(actions.Wait(self.hero))
        elif vec in dirconst.CARDINALS:
            destTile = self.hero.tile.relTile(vec)
            self.trySubmitAction( actions.ShiftStep(self.hero, destTile ))

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

    def trySubmitAction(self, action):
        self.state.rSubmitAction(action)

    def warpAdvanceTime(self):
        self.transfer(AdvanceTimeWarp(self.interf))
    def wtransferPlayerInput(self):
        pass

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

        self.reflect(self.ancestor.interf.state.activeZone.grid)

    def reflect(self, grid):
        self.grid = grid
        for pos in self.allPoses():
            self.lookup(pos).reflect(self.grid.lookup(pos))

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

        self._reflector = None

    def reflect(self, tile):
        self._reflector = tile
        return self

    @property
    def panelSize(self):
        return vecs.Vec2(3, 3)

    def drawContents(self, ren):
        if self._reflector.occupant is not None:
            ren.drawChar( (1,1), self._reflector.occupant.drawChar, fg=(255, 0, 0) )
        else:
            ren.drawChar( (1,1), " " )
