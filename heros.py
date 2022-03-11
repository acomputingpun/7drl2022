import actors, rsignals, tiles

class Hero(tiles.Occupant, actors.Actor):
    displayChar = "@"

    def tryRequestAction(self, interf):
        return interf.warpRequestAction()