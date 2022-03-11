import dirconst

class Tile():
    def __init__(self, grid, xyPos):
        self.grid = grid
        self.xyPos = xyPos
        self.terrain = None
        self.occupant = None

    def octagonalPoses(self):
        return [self.xyPos+vec for vec in dirconst.OCTAGONALS if self.grid.rectContains(self.xyPos+vec)]
    def octagonalTiles(self):
        return [self.grid.lookup(adjPos) for adjPos in self.octagonalPoses()]

    def adjacentPoses(self):
        return [self.xyPos+vec for vec in dirconst.CARDINALS if self.grid.rectContains(self.xyPos+vec)]
    def adjacentTiles(self):
        return [self.grid.lookup(adjPos) for adjPos in self.adjacentPoses()]

    def relTile(self, vec):
        return self.grid.lookup(self.xyPos+vec)

    def listContents(self):
        if self.occupant is not None:
            yield self.occupant
        return

    def setTerrain(self, terrainClass, *params):
        self.terrain = terrainClass(self, *params)

    @property
    def displayChar(self):
        if self.terrain is not None:
            return self.terrain.displayChar
        else:
            return "."

    def __repr__(self):
        return ("t{}".format(self.xyPos))

class Item():
    _holder = None
    def setHolder(self, holder):
        if self._holder is not None:
            self._holder.items.remove(self)
        self._holder = tile
        if self._holder is not None:
            self._holder.items.append(self)

class Occupant():
    displayChar = "@"
    skipDraw = False
    _tile = None

    def setTile(self, tile):
        if self._tile is not None:
            self._tile.occupant = None
        if tile is not None:
            if tile.occupant is not None:
                raise Exception()
            tile.occupant = self
        self._tile = tile

    @property
    def tile(self):
        return self._tile
    @property
    def xyPos(self):
        return self.tile.xyPos
    @property
    def grid(self):
        return self.tile.grid