import xchars, random

class Terrain():
    displayChar = ord("?")
    displayFG = (10, 10, 10)
    displayBG = (200, 200, 200)

    blocksMovement = False

    def __init__(self):
        self.tile = None

    def setTile(self, data):
        self.tile = data
    def getTile(self):
        return self.tile

class Floor(Terrain):
    displayChar = ord(".")
    blocksMovement = False

class Wall(Terrain):
    displayChar = ord("#")
    blocksMovement = True