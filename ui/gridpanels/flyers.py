import math, utils
from .. import animas, scions

class CardinalShiftFlyer(animas.Flyer):
    xyAnchor = (0,0)

    maxMS = 250
    blockingMS = 200

    def __init__(self, parent, mob, sourceTile, destTile):
        super().__init__(parent)
        self.sourceTile = sourceTile
        self.destTile = destTile

        self.mob = mob
        self.sourceDraw = self.parent.posToCenterDraw(self.sourceTile.xyPos)
        self.destDraw = self.parent.posToCenterDraw(self.destTile.xyPos)

        self.moveVec = self.destTile.xyPos - self.sourceTile.xyPos
        self.drawStepPoses = [self.sourceDraw + self.moveVec*k for k in range(0, self.parent.TILE_SPACING +1)]

    def drawOutline(self, ren):
        pass
    def drawContents(self, ren):
        stepIndex = min(math.floor(self.frac() * (self.parent.TILE_SPACING+1)), self.parent.TILE_SPACING)
        ren.drawChar(self.drawStepPoses[stepIndex], self.mob.displayChar, self.mob.displayFG)

class PathAttackFlyer(animas.Flyer):
    stepMS = 15
    tailLength = 8

    def __init__(self, parent, path):
        super().__init__(parent)
        self.pathTiles = path
        self.xyPathPoses = [tile.xyPos for tile in self.pathTiles]
        self.xyDrawPoses = self.parent.pathToDraws(self.xyPathPoses)

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