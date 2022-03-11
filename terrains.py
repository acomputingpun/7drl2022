import xchars, random

class Terrain():
    displayChar = "?"
    displayFG = (60, 120, 60)
    displayBG = (30, 30, 30)

    blocksMovement = False

    def __init__(self, tile = None):
        self.tile = tile

    def setTile(self, data):
        self.tile = data
    def getTile(self):
        return self.tile

class Floor(Terrain):
    displayChar = "."
    blocksMovement = False

class Wall(Terrain):
    displayFG = (200, 200, 200)

    displayChar = "#"
    blocksMovement = True