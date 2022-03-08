from . import warps, windows, animas, gridpanels, gridwarps
import vecs, dirconst

import math
#from . import warps, windows, gridpanels, syspanels, nonpanels, attpanels, messages, backpanels, animas
#from . import fx
#import random

class GameWindow(windows.Window):
    def __init__(self, interf):
        super().__init__(interf)

        self.gridPanel = gridpanels.GridPanel(self)
        self.msgPanel = MessagePanel(self)
        self.sidePanel = SidePanel(self)

        self.children = [self.gridPanel, self.msgPanel, self.sidePanel]

    @property
    def hero(self):
        return self.interf.state.hero

    def drawContents(self, ren):
        ren.drawText( (0,0), "hello world" )

    def debug_addLBF(self):
        debug_lbf = LoadingBarFlyer(self)
        debug_lbf.register(self.interf)
        self.children.append(debug_lbf)

    def afxShiftStep(self, mob, destTile):
        shiftFlyer = CardinalShiftFlyer(self.gridPanel, mob.tile, destTile)
        shiftFlyer.register(self.interf)
        self.interf.capture(AnimaBlockedWarp(self.interf))

    def afxDamageNumber(self, mob, damage):
        damageFlyer = DamageNumberFlyer(self.gridPanel.lookup(mob.tile.xyPos), damage)
        damageFlyer.register(self.interf)
        self.interf.capture(AnimaBlockedWarp(self.interf))

    def afxPathAttack(self, mob, atkProfile, target, path):
        "todo: more customisation for this"
        attackFlyer = PathAttackFlyer(self.gridPanel, path)
        attackFlyer.register(self.interf)
        self.interf.capture(AnimaBlockedWarp(self.interf))

    def requestActionWarp(self, interf):
        return gridwarps.RequestActionWarp(interf)

class AnimaBlockedWarp(warps.AnimaBlockedWarp):
    def warpArrowKey(self, vec, shift = False):
        print ("atw - arrow key was", vec)
    def warpOtherKey(self, key):
        print ("atw - key was", key)

from . import scions

class LoadingBarFlyer(animas.Flyer):
    xyAnchor = 40, 1
    maxMS = 1000

    def drawOutline(self, ren):
        ren.drawText((0, 0), "-" * 25)
    def drawContents(self, ren):
        ren.drawText((0, 0), "+" * math.floor(25 * self.frac()), fg = (255, 0, 0))

from . import scions
import vecs, utils

class SidePanel(scions.Panel):
    xyAnchor = (45, 0)
    _panelSize = vecs.Vec2(30, 44)

    def __init__(self, parent):
        super().__init__(parent)

    def drawOutline(self, ren):
        super().drawOutline(ren)

        for y in range(self.panelSize.y):
            ren.drawChar((0, y), "|" )

    @property
    def hero(self):
        return self.interf.state.hero

    def drawContents(self, ren):
        ren.drawText( (0, 0), "sidepanel")

class MessagePanel(scions.Panel):
    xyAnchor = (0, 44)
    _panelSize = vecs.Vec2(60, 6)

    def drawContents(self, ren):
        ren.drawText( (0, 0), "messagepanel")

class CardinalShiftFlyer(animas.Flyer):
    xyAnchor = (0,0)

    maxMS = 250
    blockingMS = 200

    def __init__(self, parent, sourceTile, destTile):
        super().__init__(parent)
        self.sourceTile = sourceTile
        self.destTile = destTile

        self.sourceDraw = self.parent.xyTileToCenter(self.sourceTile.xyPos)
        self.destDraw = self.parent.xyTileToCenter(self.destTile.xyPos)

        self.moveVec = self.destTile.xyPos - self.sourceTile.xyPos
        self.drawStepPoses = [self.sourceDraw + self.moveVec*k for k in range(0, self.parent.TILE_SPACING +1)]

    def drawOutline(self, ren):
        pass
    def drawContents(self, ren):
        stepIndex = math.floor(self.frac() * self.parent.TILE_SPACING+1)

        ren.drawChar(self.drawStepPoses[stepIndex], "@", fg = (255, 255, 0))

class PathAttackFlyer(animas.Flyer):
    stepMS = 15
    tailLength = 8

    def __init__(self, parent, path):
        super().__init__(parent)
        self.pathTiles = path
        self.xyPathPoses = [tile.xyPos for tile in self.pathTiles]

        self.xyDrawPoses = []
        for (xySource, xyDest) in zip( self.xyPathPoses[:-1], self.xyPathPoses[1:] ):
            vec = xyDest - xySource
            self.xyDrawPoses += [self.parent.xyTileToCenter(xySource) + (vec * k) for k in range(self.parent.TILE_SPACING)]

        self.xyDrawPoses = self.xyDrawPoses + [self.parent.xyTileToCenter(self.xyPathPoses[-1])]

        self.blockingMS = self.stepMS * len(self.xyDrawPoses)
        self.maxMS = self.stepMS * (len(self.xyDrawPoses) + self.tailLength)

    def drawContents(self, ren):
        pathHeadIndex = self.pathHeadIndex()

        for k, xyDraw in enumerate(self.xyDrawPoses):
            headDist = pathHeadIndex - k

            if headDist < 0:
                break
            elif headDist < 2:
                glow = 1
            elif headDist < self.tailLength:
                glow = 1/(headDist / 2)
            else:
                continue    

            ren.drawChar( xyDraw, "o", fg= utils.interp3( (0, 0, 128), glow, (128, 128, 255)) )

    def pathHeadIndex(self):
        return self.MS() / self.stepMS

class DamageNumberFlyer(animas.Flyer):
    xyAnchor = (1,1)
    maxMS = 500
    blockingMS = 0

    def __init__(self, parent, damage):
        super().__init__(parent)
        self.damage = damage

    def drawContents(self, ren):
        ren.drawChar( (0, 0), "2", fg = (255, 0, 0), bg = (128, 0, 0))