import vecs, dirconst, utils
import tiles

class Grid():
    def __init__(self, xySize):
        (self.xSize, self.ySize) = self.xySize = vecs.Vec2(xySize)
        self.matrix = [[self.createTile(vecs.Vec2(x,y)) for y in range(self.ySize)] for x in range(self.xSize)]

    def createTile(self, xyPos):
        return tiles.Tile(self, xyPos)

    def lookup(self, xyPos):
        if self.rectContains(xyPos):
            return self.matrix[xyPos[0]][xyPos[1]]
        else:
            return None
    def put(self, xyPos, data):
        self.matrix[xyPos[0]][xyPos[1]] = data
    def rectContains(self, xyPos):
        return utils.rectContains(((0,0), self.xySize), xyPos)

    def allPoses(self):
        return utils.allPoses((0,0), self.xySize)
    def allTiles(self):
        for pos in self.allPoses():
            yield self.lookup(pos)

    def debugPrint(self):
        for y in range(self.ySize):
            for x in range(self.xSize):
                tile = self.lookup((x,y))
                if tile.terrain is not None:
                    print(tile.terrain.debugChar, end="")
                else:
                    print("?", end="")
            print("")
