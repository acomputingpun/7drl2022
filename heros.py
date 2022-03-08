import actors, rsignals, tiles

class Hero(tiles.Occupant, actors.Actor):
    drawChar = "@"

    def tryRequestAction(self, interf):
        return interf.warpRequestAction()