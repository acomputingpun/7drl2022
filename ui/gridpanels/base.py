import vecs, utils, dirconst
from .. import scions, animas
from . import flyers

import random

class GridPanel(scions.Panel):
    TILE_SPACING = 4
    TILES_ON_GRID = 11
    xyAnchor = (1, 8)
    _panelSize = vecs.Vec2(43, 43)

    NUM_TILE_REDRAW_GROUPS = 7

    def __init__(self, parent):
        super().__init__(parent)

        self.trMatrix = [[TileReflection(self, vecs.Vec2(x,y)) for y in range(self.TILES_ON_GRID)] for x in range(self.TILES_ON_GRID)]
        self.children = [k for k in self.allTiles()]

        self.reflect(self.ancestor.interf.state.activeZone.grid)

        self.tileGlowAnima = animas.Periodic(self.interf, periodMS = 5000)
        self.curRedrawGroupID = 0
        self.setupTileRedrawGroups()

    def setupTileRedrawGroups(self):
        for (tileIndex, tile) in enumerate(self.allTiles()):
            if tileIndex % self.NUM_TILE_REDRAW_GROUPS == 0:
                redrawGroupIDs = [k for k in range(self.NUM_TILE_REDRAW_GROUPS)] 
                random.shuffle(redrawGroupIDs)
            tile.redrawGroup = redrawGroupIDs[tileIndex % self.NUM_TILE_REDRAW_GROUPS]

            tile.resetGlowValue()

    def drawChildren(self, ren):
        self.curRedrawGroupID = (self.curRedrawGroupID + 1) % self.NUM_TILE_REDRAW_GROUPS
        super().drawChildren(ren)

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

    def drawContents(self, ren):
        for xyDraw in utils.range2(self.panelSize):
            ren.drawChar( xyDraw, "?", fg = (30, 60, 30), bg = (0, 20, 0) )

    def posToNWDraw(self, xyTile):
        return (xyTile * self.TILE_SPACING)
    def posToCenterDraw(self, xyTile):
        return vecs.Vec2(1, 1) + self.posToNWDraw(xyTile)

    def pathToDraws(self, pathPoses):
        xyDraws = []

        for (pathSource, pathDest) in zip( pathPoses[:-1], pathPoses[1:] ):
            vec = pathDest - pathSource
            xyDraws += [self.posToCenterDraw(pathSource) + (vec * k) for k in range(self.TILE_SPACING)]

        xyDraws.append (self.posToCenterDraw(pathPoses[-1]))
        return xyDraws

    def zoneToTileDraws(self, zonePoses):
        xyDraws = []
        for zonePos in zonePoses:
            zpDraw = self.posToCenterDraw(zonePos)
            xyDraws = xyDraws + [vec+zpDraw for vec in dirconst.NONAGONALS]
        return xyDraws

    def zoneToOutlineDraws(self, zonePoses):
        zpSet = set(zonePoses)
        xyDraws = []
        for zonePos in zpSet:
            zpDraw = self.posToCenterDraw(zonePos)

            for diag in dirconst.DIAGONALS:
                if zonePos + diag not in zpSet:
                    xyDraws.append( diag*2 + zpDraw )

            for card in dirconst.CARDINALS:
                if zonePos + card not in zpSet:
                    xyDraws.append( card*2 + zpDraw )
                    xyDraws.append( card*2 + zpDraw + dirconst.ROT_CW[card] )
                    xyDraws.append( card*2 + zpDraw + dirconst.ROT_CCW[card] )
        return xyDraws

    def zoneToGutterDraws(self, zonePoses):
        zpSet = set(zonePoses)
        xyDraws = set()
        for zonePos in zpSet:
            zpDraw = self.posToCenterDraw(zonePos)

            for diag in dirconst.DIAGONALS:
                if (zonePos + diag in zpSet) and (zonePos + (diag.x, 0) in zpSet) and (zonePos + (0, diag.y) in zpSet):
                    xyDraws.add( zpDraw + diag*2 )

            for card in dirconst.CARDINALS:
                if zonePos + card in zpSet:
                    xyDraws.add( card*2 + zpDraw )
                    xyDraws.add( card*2 + zpDraw + dirconst.ROT_CW[card] )
                    xyDraws.add( card*2 + zpDraw + dirconst.ROT_CCW[card] )
        return [k for k in xyDraws]




    def afxShiftStep(self, mob, destTile):
        shiftFlyer = flyers.CardinalShiftFlyer(self, mob.tile, destTile)
        shiftFlyer.register(self.interf)

    def afxDamageNumber(self, mob, damage):
        damageFlyer = flyers.DamageNumberFlyer(self.lookup(mob.tile.xyPos), damage)
        damageFlyer.register(self.interf)

    def afxPathAttack(self, mob, atkProfile, target, path):
        "todo: more customisation for this"
        attackFlyer = flyers.PathAttackFlyer(self, path)
        attackFlyer.register(self.interf)

class TileReflection(scions.Panel):
    _panelSize = vecs.Vec2(3, 3)

    def __init__(self, parent, xyTile):
        super().__init__(parent)
        self.xyTile = xyTile
        self.xyAnchor = self.parent.posToNWDraw(xyTile)

        self._reflector = None
        self.children = []

        self.redrawGroup = 0
        self.savedGlowValue = 0

    def reflect(self, tile):
        self._reflector = tile
        return self

    def resetGlowValue(self):
        self.savedGlowValue = 0.03 * self.parent.tileGlowAnima.sawtoothFrac()

    def drawOutline(self, ren):
        if self.parent.curRedrawGroupID == self.redrawGroup:
            self.resetGlowValue()

        baseBG = self._reflector.terrain.displayBG
        baseFG = self._reflector.terrain.displayFG

        glowBG = utils.interp3( baseBG, self.savedGlowValue, (255, 255, 255) )
        glowFG = utils.interp3( baseFG, self.savedGlowValue, (255, 255, 255) )

        for xy in utils.range2(self.panelSize):
            ren.drawChar( xy, self._reflector.displayChar, fg = glowFG, bg = glowBG )

    def drawContents(self, ren):
        if self._reflector.occupant is not None:
            ren.drawChar( (1,1), self._reflector.occupant.displayChar, fg=(255, 0, 0) )
        else:
            pass
#            ren.drawChar( (1,1), " " )


class ZoneOverlay(scions.Scion):
    bgDebug = (255, 255, 255)

    def __init__(self, parent, zonePoses):
        super().__init__(parent)

        self.innerDraws = self.parent.zoneToTileDraws(zonePoses) + self.parent.zoneToGutterDraws(zonePoses)
        self.outlineDraws = self.parent.zoneToOutlineDraws(zonePoses)

    def drawOutline(self, ren):
        for xyDraw in self.outlineDraws:
            ren.drawChar( xyDraw, "#" )

    def drawContents(self, ren):
        for xyDraw in self.innerDraws:
            ren.drawChar( xyDraw, "z" )

class AnimatedZoneOverlay(ZoneOverlay, animas.Anima):
    stepMS = 25
    blockingMS = 0

    def __init__(self, parent, zonePoses, zoneSourcePos):
        super().__init__(parent, zonePoses)
        self.xySourceDraw = self.parent.posToCenterDraw(zoneSourcePos)
        self.maxMS = self.stepMS * self.parent.TILE_SPACING * (max( utils.distMan(zonePos, zoneSourcePos) for zonePos in zonePoses) + 2)

    def drawOutline(self, ren):
        for xyDraw in self.outlineDraws:

            if utils.distMan( xyDraw, self.xySourceDraw ) < self.MS()/self.stepMS:
                ren.drawChar( xyDraw, "#" )

    def drawContents(self, ren):
        headDist = self.growHeadDist()

        for xyDraw in self.innerDraws:
            drawDist = utils.distMan( xyDraw, self.xySourceDraw )
            fromHeadDist = headDist - drawDist

            if 5 > fromHeadDist > 0:
                ren.drawChar( xyDraw, "z" )

    def growHeadDist(self):
        return (self.MS() / self.stepMS)