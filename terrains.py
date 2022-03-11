import xchars, random

class Terrain():
    displayChar = "?"
    displayFG = (60, 120, 60)
    displayBG = (20, 40, 20)

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
    displayChar = "#"
    blocksMovement = True