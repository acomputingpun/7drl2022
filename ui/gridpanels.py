from . import scions
import vecs, utils

class GridPanel(scions.Panel):
    TILE_SPACING = 4
    TILES_ON_GRID = 11
    xyAnchor = (1, 1)
    _panelSize = vecs.Vec2(43, 43)

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

    def drawContents(self, ren):
        ren.drawText( (0, 0), "gridpanel")

    def xyTileToNW(self, xyTile):
        return (xyTile * self.TILE_SPACING)
    def xyTileToCenter(self, xyTile):
        return self.xyTileToNW(xyTile) + (1, 1)

class TileReflection(scions.Panel):
    _panelSize = vecs.Vec2(3, 3)

    def __init__(self, parent, xyTile):
        super().__init__(parent)
        self.xyTile = xyTile
        self.xyAnchor = self.parent.xyTileToNW(xyTile)

        self._reflector = None

    def reflect(self, tile):
        self._reflector = tile
        return self

    def drawContents(self, ren):
        if self._reflector.occupant is not None:
            ren.drawChar( (1,1), self._reflector.occupant.drawChar, fg=(255, 0, 0) )
        else:
            ren.drawChar( (1,1), " " )

class GridCursor(scions.Scion):
    fgDebug = (255, 255, 255)
    xyAnchor = (0, 0)

    def __init__(self, parent, xyStartTile):
        super().__init__(parent)
        self.xyTile = self.xyStartTile = xyStartTile
    @property
    def grid(self):
        return self.parent.grid

    def drawOutline(self, ren):
        pass
    def drawContents(self, ren):
        xyDraw = self.parent.xyTileToNW(self.xyTile)

        ren.drawChar (xyDraw+(0, 0), "*", fg = self.fgDebug)
        ren.drawChar (xyDraw+(2, 0), "*", fg = self.fgDebug)
        ren.drawChar (xyDraw+(0, 2), "*", fg = self.fgDebug)
        ren.drawChar (xyDraw+(2, 2), "*", fg = self.fgDebug)

    def shift(self, vec):
        xyNew = self.xyTile + vec
        self.jumpTo(xyNew)

    def jumpTo(self, xyNew):
        if self.grid.rectContains(xyNew):
            self.xyTile = xyNew

    @property
    def tile(self):
        return self.grid.lookup(self.xyTile)

class TrailCursor(GridCursor):
    xyAnchor = (0, 0)

    def __init__(self, parent, xyStartTile):
        super().__init__(parent, xyStartTile)
        self.xyPathNodes = [self.xyStartTile]

    def shift(self, vec):
        xyNew = self.xyTile + vec
        if self.grid.rectContains(xyNew):
            self.xyTile = xyNew

            if xyNew in self.xyPathNodes:
                self.xyPathNodes = self.xyPathNodes[: self.xyPathNodes.index(xyNew)+1]
            else:
                self.xyPathNodes.append(xyNew)

    def drawContents(self, ren):
        for xyPathNode in self.xyPathNodes:
            ren.drawChar( self.parent.xyTileToCenter(xyPathNode), "!", fg = self.fgDebug )
        super().drawContents(ren)

    def pathTiles(self):
        return [self.grid.lookup(xyPathNode) for xyPathNode in self.xyPathNodes]

class ExamineCursor(GridCursor):
    fgDebug = (255, 255, 0)

class SelectAttackCursor(TrailCursor):
    fgDebug = (255, 0, 0)
